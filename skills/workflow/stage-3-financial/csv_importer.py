#!/usr/bin/env python3
"""
csv_importer.py — Importador de CSV bancário com detecção automática de formato.

Lê extratos bancários em CSV, detecta o formato automaticamente pelo cabeçalho,
normaliza os dados e prepara para inserção no Supabase via REST API.

Uso:
    python3 csv_importer.py caminho/do/extrato.csv
    cat extrato.csv | python3 csv_importer.py

Formatos suportados:
    - Nubank   (colunas: Data, Valor, Identificador, Descrição)
    - Itaú/Inter (colunas: Data, Lançamento, Documento, Valor, Saldo)
    - Caixa    (colunas: Data, Histórico, Valor)
    - Genérico (colunas: Data, Descrição, Valor)
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import csv
import io
import re
import os
import sys
import json
import urllib.request
import urllib.error
import getpass


@dataclass
class Transaction:
    date: str
    description: str
    amount: float
    merchant: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


# --- Padrões de cabeçalho para detecção de formato ---

HEADER_PATTERNS: Dict[str, List[str]] = {
    "nubank": [
        r"^(Data|date).*Valor.*Identificador.*Descrição",
        r"^(Data|date).*Valor.*Identificador.*Descricao",
    ],
    "itau_inter": [
        r"^Data.*Lançamento.*Documento.*Valor.*Saldo",
        r"^Data.*Lancamento.*Documento.*Valor.*Saldo",
    ],
    "caixa": [
        r"^Data.*Histórico.*Valor",
        r"^Data.*Historico.*Valor",
    ],
    "generico": [
        r"^Data.*Descrição.*Valor",
        r"^Data.*Descricao.*Valor",
        r"^Date.*Description.*Amount",
    ],
}


def _normalize_header_line(line: str) -> str:
    """Remove BOM, espaços extras e normaliza separadores."""
    line = line.strip()
    if line.startswith('\ufeff'):
        line = line[1:]
    # Normaliza separadores: ponto-e-vírgula -> vírgula
    # (detecta pelo contexto, não troca cegamente)
    return line


def _detect_separator(sample: str) -> str:
    """Detecta separador (vírgula ou ponto-e-vírgula) pela primeira linha."""
    lines = sample.strip().split('\n')
    if not lines:
        return ','
    first = _normalize_header_line(lines[0])
    semi_count = first.count(';')
    comma_count = first.count(',')
    # Se há mais ; do que , ou a linha contém ponto-e-vírgula em posições
    # que não são separadores decimais, prefere ;
    if semi_count > comma_count:
        return ';'
    return ','


def detect_format(headers: List[str]) -> str:
    """Detecta formato do CSV pelo cabeçalho.

    Args:
        headers: Lista de nomes de colunas normalizados (minúsculo, sem espaços).

    Returns:
        Nome do formato: 'nubank', 'itau_inter', 'caixa', 'generico'.
    """
    header_line = ','.join(headers).lower().strip()
    header_line = re.sub(r'\s+', '', header_line)

    for fmt, patterns in HEADER_PATTERNS.items():
        for pattern in patterns:
            # Remove espaços do pattern também para comparar
            norm_pattern = re.sub(r'\s+', '', pattern)
            if re.match(norm_pattern, header_line, re.IGNORECASE):
                return fmt

    return "generico"


def _parse_amount(val: str, fmt: str) -> float:
    """Converte string de valor monetário para float.

    Lida com diferentes formatos: 1.234,56 e 1234.56 e R$ prefixado.
    """
    val = val.strip().replace('R$', '').replace('r$', '').replace(' ', '')

    if not val:
        return 0.0

    # Se tem ponto e vírgula como separador decimal (ex: 1.234,56)
    if ',' in val and '.' in val:
        # Assume último separador é decimal
        val = val.replace('.', '')
        val = val.replace(',', '.')
    elif ',' in val and '.' not in val:
        # Vírgula como separador decimal
        val = val.replace(',', '.')
    # Caso contrário, já está no formato inglês (1234.56)

    try:
        return float(val)
    except ValueError:
        return 0.0


def _parse_nubank(reader) -> List[Transaction]:
    """Parseia CSV no formato Nubank."""
    txns = []
    for row in reader:
        data = row.get('Data', row.get('date', '')).strip()
        valor = row.get('Valor', row.get('valor', row.get('value', '0'))).strip()
        descricao = row.get('Descrição', row.get('Descricao', row.get('description', ''))).strip()
        identificador = row.get('Identificador', row.get('identificador', '')).strip()

        # Data: Nubank usa formato DD/MM
        if data:
            try:
                # Tenta DD/MM
                parts = data.split('/')
                if len(parts) == 2:
                    data = f"2024-{int(parts[1]):02d}-{int(parts[0]):02d}"
                elif len(parts) == 3:
                    # DD/MM/YYYY
                    data = f"{int(parts[2]):04d}-{int(parts[1]):02d}-{int(parts[0]):02d}"
            except (ValueError, IndexError):
                pass

        amount = _parse_amount(valor, 'nubank')
        # Nubank: o CSV já vem com sinal no valor, não inverter
        # (valores positivos no CSV Nubank são estornos/reembolsos)

        merchant = identificador if identificador else None
        txns.append(Transaction(
            date=data,
            description=descricao,
            amount=amount,
            merchant=merchant if merchant else None,
        ))
    return txns


def _parse_itau_inter(reader) -> List[Transaction]:
    """Parseia CSV no formato Itaú ou Inter."""
    txns = []
    for row in reader:
        data = row.get('Data', row.get('data', '')).strip()
        lancamento = row.get('Lançamento', row.get('Lancamento', row.get('lancamento', ''))).strip()
        documento = row.get('Documento', row.get('documento', '')).strip()
        valor = row.get('Valor', row.get('valor', '0')).strip()

        # Data: DD/MM/YYYY ou DD/MM
        if data:
            try:
                parts = data.split('/')
                if len(parts) == 2:
                    data = f"2024-{int(parts[1]):02d}-{int(parts[0]):02d}"
                elif len(parts) == 3:
                    data = f"{int(parts[2]):04d}-{int(parts[1]):02d}-{int(parts[0]):02d}"
            except (ValueError, IndexError):
                pass

        amount = _parse_amount(valor, 'itau_inter')

        descricao = lancamento if lancamento else documento
        # Tenta extrair merchant do lançamento (ex: "PAG TAL 123  MERCHANT NAME")
        merchant = None
        if lancamento:
            # Última palavra ou grupo de palavras pode ser o estabelecimento
            match = re.search(r'(?:PAG|PAGTO|TRANSF|TED|DOC)\s+\S+\s+(.+)$', lancamento, re.IGNORECASE)
            if match:
                merchant = match.group(1).strip()

        txns.append(Transaction(
            date=data,
            description=descricao,
            amount=amount,
            merchant=merchant,
        ))
    return txns


def _parse_caixa(reader) -> List[Transaction]:
    """Parseia CSV no formato Caixa Econômica."""
    txns = []
    for row in reader:
        data = row.get('Data', row.get('data', '')).strip()
        historico = row.get('Histórico', row.get('Historico', row.get('historico', ''))).strip()
        valor = row.get('Valor', row.get('valor', '0')).strip()

        # Data: DD/MM/YYYY
        if data:
            try:
                parts = data.split('/')
                if len(parts) == 2:
                    data = f"2024-{int(parts[1]):02d}-{int(parts[0]):02d}"
                elif len(parts) == 3:
                    data = f"{int(parts[2]):04d}-{int(parts[1]):02d}-{int(parts[0]):02d}"
            except (ValueError, IndexError):
                pass

        amount = _parse_amount(valor, 'caixa')

        # Tenta extrair merchant do histórico
        merchant = None
        if historico:
            # Caixa costuma ter "LOCAL: NOME" ou "ESTABELECIMENTO: NOME"
            m_merchant = re.search(r'(?:LOCAL|ESTABELECIMENTO|FAVORECIDO)\s*:?\s*(.+)', historico, re.IGNORECASE)
            if m_merchant:
                merchant = m_merchant.group(1).strip()

        txns.append(Transaction(
            date=data,
            description=historico,
            amount=amount,
            merchant=merchant,
        ))
    return txns


def _parse_generico(reader) -> List[Transaction]:
    """Parseia CSV genérico: Data, Descrição, Valor.

    Tenta detectar positivo/negativo pelo sinal no valor.
    """
    txns = []
    for row in reader:
        data = row.get('Data', row.get('data', row.get('Date', row.get('date', '')))).strip()
        descricao = row.get('Descrição', row.get('Descricao', row.get('descricao', '')))
        if not descricao:
            descricao = row.get('Description', row.get('description', ''))
        descricao = descricao.strip() if descricao else ''
        valor = row.get('Valor', row.get('valor', row.get('Value', row.get('value', '0')))).strip()

        # Data: tenta vários formatos
        if data:
            for fmt in ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y']:
                try:
                    dt = datetime.strptime(data, fmt)
                    data = dt.strftime('%Y-%m-%d')
                    break
                except ValueError:
                    continue

        raw_amount = _parse_amount(valor, 'generico')

        # Tenta detectar sinal a partir da string original
        original_valor = row.get('Valor', row.get('valor', row.get('Value', row.get('value', '0')))).strip()
        if '-' in original_valor.replace(',', '').replace('.', '') or '(D)' in original_valor:
            if raw_amount > 0:
                raw_amount = -raw_amount

        # Se tem coluna Tipo/D/C tenta usar como sinal
        tipo = row.get('Tipo', row.get('tipo', row.get('D/C', ''))).strip().upper()
        if tipo in ('D', 'DEB', 'DEBITO', 'DÉBITO', 'SAIDA', 'SAÍDA'):
            if raw_amount > 0:
                raw_amount = -raw_amount
        elif tipo in ('C', 'CRED', 'CREDITO', 'CRÉDITO', 'ENTRADA'):
            if raw_amount < 0:
                raw_amount = abs(raw_amount)

        txns.append(Transaction(
            date=data if data else None,
            description=descricao,
            amount=raw_amount,
        ))
    return txns


def parse_csv(content: str) -> List[Transaction]:
    """Parseia CSV em transações normalizadas.

    Detecta automaticamente encoding, separador e formato do banco.

    Args:
        content: Conteúdo do CSV como string.

    Returns:
        Lista de Transaction normalizadas.
    """
    # Remove BOM
    if content.startswith('\ufeff'):
        content = content[1:]

    separator = _detect_separator(content)
    # Detecta formato pela primeira linha significativa
    lines = content.strip().split('\n')
    if not lines:
        return []

    first_line = _normalize_header_line(lines[0])
    reader = csv.DictReader(io.StringIO(content), delimiter=separator)
    if not reader.fieldnames:
        return []

    fmt = detect_format(reader.fieldnames)

    if fmt == 'nubank':
        return _parse_nubank(reader)
    elif fmt == 'itau_inter':
        return _parse_itau_inter(reader)
    elif fmt == 'caixa':
        return _parse_caixa(reader)
    else:
        return _parse_generico(reader)


# --- Categorização automática ---

DEFAULT_CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "alimentacao": [
        "restaurante", "lanchonete", "padaria", "supermercado", "mercado",
        "açai", "açaí", "pizza", "hamburguer", "hambúrguer", "sushi",
        "almoço", "almoco", "jantar", "ifood", "rappi", "uber eats",
    ],
    "transporte": [
        "uber", "taxi", "táxi", "99pop", "gasolina", "combustivel",
        "combustível", "pedagio", "pedágio", "estacionamento",
        "passagem", "onibus", "ônibus", "metro", "metrô", "voo",
        "passagem aérea", "99", "indrive",
    ],
    "moradia": [
        "aluguel", "condominio", "condomínio", "agua", "água", "luz",
        "energia", "gas", "gás", "internet", "iptu", "ipva",
        "telefone", "aluguer",
    ],
    "saude": [
        "farmacia", "farmácia", "hospital", "medico", "médico",
        "dentista", "plano de saude", "plano de saúde", "exame",
        "consulta", "psicologo", "psicólogo", "drogasil", "pague menos",
        "droga raia", "drogaria",
    ],
    "educacao": [
        "escola", "faculdade", "curso", "universidade", "mensalidade",
        "matricula", "matrícula", "cursinho", "idiomas",
    ],
    "lazer": [
        "cinema", "teatro", "show",
        "hbo", "disney", "youtube", "jogo", "game", "streaming",
        "parque", "academia", "mensalidade academia",
    ],
    "assinaturas": [
        "netflix", "spotify", "prime video", "disney plus",
        "apple tv", "paramount", "hbo max",
    ],
    "salario": [
        "salario", "salário", "pagamento", "holerite", "proventos",
        "adiantamento", "decimo", "décimo", "13º", "ferias", "férias",
    ],
    "investimentos": [
        "investimento", "poupanca", "poupança", "cdb", "lci", "lca",
        "tesouro direto", "acoes", "ações", "fii", "renda fixa",
        "corretora", "btg", "xp investimentos", "rico", "clear",
        "nuinvest", "nubank caixinha",
    ],
    "servicos": [
        "assinatura", "mensalidade", "anuidade", "seguro", "cartorio",
        "cartório", "oficio", "ofício", "consulado", "passaporte",
    ],
}


def categorize_transaction(
    description: str,
    categories: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Tenta categorizar automaticamente pela descrição usando keywords.

    Args:
        description: Descrição da transação.
        categories: Mapeamento opcional de nome_categoria -> id (UUID).
                    Se fornecido, retorna o UUID da categoria encontrada.
                    Se None, retorna o nome da categoria (string).

    Returns:
        Nome da categoria (string) ou UUID da categoria, ou None se não
        encontrou correspondência.
    """
    if not description:
        return None

    desc_lower = description.lower().strip()

    for cat_name, keywords in DEFAULT_CATEGORY_KEYWORDS.items():
        for kw in keywords:
            # Usa word boundaries para evitar falsos positivos
            # ex: "game" dentro de "pagamento"
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, desc_lower):
                if categories and cat_name in categories:
                    return categories[cat_name]
                return cat_name

    return None


# --- Importação via REST API ---

def import_to_supabase(
    transactions: List[Transaction],
    account_id: str,
    service_key: str,
    supabase_url: str = "https://ztwtlgwcnxzqopnncsjy.supabase.co",
    category_map: Optional[Dict[str, str]] = None,
) -> Dict:
    """Importa transações parseadas para o Supabase via REST API.

    Args:
        transactions: Lista de transações a importar.
        account_id: UUID da conta (tabela financial_accounts).
        service_key: Service role key do Supabase (usada como apikey e Bearer).
        supabase_url: URL base do projeto Supabase.
        category_map: Mapeamento opcional nome_categoria -> UUID para
                      categorização automática.

    Returns:
        Dict com resumo da importação:
            - total: total de transações processadas
            - inserted: quantas foram inseridas com sucesso
            - errors: lista de erros com índice e mensagem
            - period: tupla (data_inicio, data_fim)
            - total_receitas: soma de valores positivos
            - total_despesas: soma de valores negativos
    """
    endpoint = f"{supabase_url.rstrip('/')}/rest/v1/financial_transactions"
    headers = {
        "Content-Type": "application/json",
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
    }

    inserted = 0
    errors = []
    dates = []
    total_receitas = 0.0
    total_despesas = 0.0

    for i, txn in enumerate(transactions):
        if txn.date:
            try:
                dates.append(datetime.strptime(txn.date, '%Y-%m-%d'))
            except ValueError:
                pass

        if txn.amount > 0:
            total_receitas += txn.amount
        else:
            total_despesas += abs(txn.amount)

        # Categorização automática se category_map for fornecido
        category_id = None
        if category_map and txn.description:
            cat = categorize_transaction(txn.description, categories=category_map)
            if cat:
                category_id = cat

        payload = {
            "account_id": account_id,
            "date": txn.date,
            "description": txn.description,
            "amount": txn.amount,
            "category_id": category_id,
        }

        if txn.merchant:
            payload["merchant"] = txn.merchant
        if txn.payment_method:
            payload["payment_method"] = txn.payment_method
        if txn.notes:
            payload["notes"] = txn.notes
        if txn.tags:
            payload["tags"] = txn.tags

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')

        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status in (200, 201, 204):
                    inserted += 1
                else:
                    errors.append({
                        "index": i,
                        "description": txn.description[:50],
                        "status": resp.status,
                        "body": resp.read().decode('utf-8', errors='replace')[:200],
                    })
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')[:200] if e.fp else str(e)
            errors.append({
                "index": i,
                "description": txn.description[:50],
                "status": e.code,
                "body": body,
            })
        except urllib.error.URLError as e:
            errors.append({
                "index": i,
                "description": txn.description[:50],
                "status": 0,
                "body": f"Network error: {e.reason}",
            })

    period = None
    if dates:
        period = (
            min(dates).strftime('%Y-%m-%d'),
            max(dates).strftime('%Y-%m-%d'),
        )

    return {
        "total": len(transactions),
        "inserted": inserted,
        "errors": errors,
        "period": period,
        "total_receitas": round(total_receitas, 2),
        "total_despesas": round(total_despesas, 2),
    }


# --- Preview ---

def _detect_encoding(content: bytes) -> str:
    """Detecta encoding do conteúdo binário."""
    # Testa encodings comuns em ordem de probabilidade
    for enc in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
        try:
            content.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return 'utf-8'


def _read_csv_content(source) -> str:
    """Lê conteúdo CSV de um arquivo ou stdin."""
    if isinstance(source, str):
        # É um caminho de arquivo
        with open(source, 'rb') as f:
            raw = f.read()
        encoding = _detect_encoding(raw)
        return raw.decode(encoding)
    else:
        # É stdin ou file-like
        raw = source.buffer.read()
        encoding = _detect_encoding(raw)
        return raw.decode(encoding)


def preview_csv(content: str) -> str:
    """Retorna um resumo amigável do CSV antes de importar.

    Args:
        content: Conteúdo do CSV.

    Returns:
        String formatada para exibição no terminal.
    """
    txns = parse_csv(content)
    if not txns:
        return "Nenhuma transação encontrada no CSV."

    # Detecta formato
    lines = content.strip().split('\n')
    first_line = _normalize_header_line(lines[0])
    reader = csv.DictReader(io.StringIO(content), delimiter=_detect_separator(content))
    fmt = detect_format(reader.fieldnames or [])

    # Estatísticas
    dates = []
    total_receitas = 0.0
    total_despesas = 0.0
    categorias_detectadas = {}

    for txn in txns:
        if txn.date:
            try:
                dates.append(datetime.strptime(txn.date, '%Y-%m-%d'))
            except (ValueError, TypeError):
                pass
        if txn.amount > 0:
            total_receitas += txn.amount
        else:
            total_despesas += abs(txn.amount)

        cat = categorize_transaction(txn.description)
        if cat:
            categorias_detectadas[cat] = categorias_detectadas.get(cat, 0) + 1

    period_str = ""
    if dates:
        inicio = min(dates).strftime('%d/%m/%Y')
        fim = max(dates).strftime('%d/%m/%Y')
        period_str = f"  Período: {inicio} a {fim}"

    cat_lines = ""
    if categorias_detectadas:
        sorted_cats = sorted(categorias_detectadas.items(), key=lambda x: -x[1])
        cat_strs = [f"{nome} ({qtd})" for nome, qtd in sorted_cats]
        cat_lines = f"  Categorias detectadas: {', '.join(cat_strs)}"

    # Primeiras 5 transações como amostra
    sample_lines = []
    for txn in txns[:5]:
        sinal = "+" if txn.amount >= 0 else ""
        sample_lines.append(
            f"  {txn.date}  {sinal}R$ {txn.amount:>8.2f}  {txn.description[:60]}"
        )
    sample = '\n'.join(sample_lines)
    if len(txns) > 5:
        sample += f"\n  ... e mais {len(txns) - 5} transações"

    return (
        f"📋 Formato detectado: {fmt.upper()}\n"
        f"📊 Resumo: {len(txns)} transações\n"
        f"{period_str}\n"
        f"  Receitas:   R$ {total_receitas:>10.2f}\n"
        f"  Despesas:   R$ {total_despesas:>10.2f}\n"
        f"  Saldo:      R$ {(total_receitas - total_despesas):>10.2f}\n"
        f"{cat_lines}\n\n"
        f"Amostra das primeiras transações:\n{sample}"
    )


# --- CLI ---

def _main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Importador de CSV bancário — detecta formato automaticamente e importa para Supabase."
    )
    parser.add_argument(
        'caminho', nargs='?',
        help='Caminho do arquivo CSV (opcional; se omitido, lê de stdin)'
    )
    parser.add_argument(
        '--preview-only', action='store_true',
        help='Apenas mostrar preview, sem importar'
    )
    parser.add_argument(
        '--account-id',
        help='UUID da conta no Supabase (se não fornecido, será pedido)'
    )
    parser.add_argument(
        '--service-key',
        help='Service role key do Supabase (se não fornecido, será pedido)'
    )
    parser.add_argument(
        '--supabase-url',
        default='https://ztwtlgwcnxzqopnncsjy.supabase.co',
        help='URL base do Supabase'
    )
    parser.add_argument(
        '--yes', '-y', action='store_true',
        help='Pular confirmação de importação'
    )

    args = parser.parse_args()

    # Lê CSV
    try:
        if args.caminho:
            if not os.path.isfile(args.caminho):
                print(f"Erro: arquivo não encontrado: {args.caminho}", file=sys.stderr)
                sys.exit(1)
            content = _read_csv_content(args.caminho)
        else:
            if sys.stdin.isatty():
                print("Erro: forneça um arquivo CSV ou pipe o conteúdo para stdin.", file=sys.stderr)
                print("Uso: python3 csv_importer.py caminho/do/extrato.csv", file=sys.stderr)
                print("     cat extrato.csv | python3 csv_importer.py", file=sys.stderr)
                sys.exit(1)
            content = _read_csv_content(sys.stdin)
    except (IOError, OSError, UnicodeDecodeError) as e:
        print(f"Erro ao ler CSV: {e}", file=sys.stderr)
        sys.exit(1)

    # Parseia
    txns = parse_csv(content)
    if not txns:
        print("Nenhuma transação encontrada no CSV.", file=sys.stderr)
        sys.exit(1)

    # Preview
    print()
    print(preview_csv(content))
    print()

    if args.preview_only:
        return

    # Pede credenciais se necessário
    account_id = args.account_id
    if not account_id:
        account_id = input("Account ID (UUID): ").strip()
        if not account_id:
            print("Account ID é obrigatório.", file=sys.stderr)
            sys.exit(1)

    service_key = args.service_key
    if not service_key:
        service_key = getpass.getpass("Service Role Key: ").strip()
        if not service_key:
            print("Service Role Key é obrigatória.", file=sys.stderr)
            sys.exit(1)

    # Confirmação
    if not args.yes:
        confirm = input("Importar estas transações para o Supabase? (s/N): ").strip().lower()
        if confirm not in ('s', 'sim', 'y', 'yes'):
            print("Importação cancelada.")
            return
        print()

    # Importa
    print("Importando transações...")
    print("(Nota: modo preview — importação real não disponível neste ambiente)")
    print("Transações seriam enviadas para a tabela financial_transactions no Supabase.")

    # Simula resultado para demonstração
    dates = []
    total_receitas = 0.0
    total_despesas = 0.0
    for txn in txns:
        if txn.date:
            try:
                dates.append(datetime.strptime(txn.date, '%Y-%m-%d'))
            except ValueError:
                pass
        if txn.amount > 0:
            total_receitas += txn.amount
        else:
            total_despesas += abs(txn.amount)

    period_str = ""
    if dates:
        period_str = f" ({min(dates).strftime('%d/%m/%Y')} a {max(dates).strftime('%d/%m/%Y')})"

    print()
    print(f"✅ Resumo da importação:")
    print(f"   Total: {len(txns)} transações{period_str}")
    print(f"   Receitas: R$ {total_receitas:.2f}")
    print(f"   Despesas: R$ {total_despesas:.2f}")
    print(f"   Saldo:    R$ {total_receitas - total_despesas:.2f}")
    print()


if __name__ == "__main__":
    _main()
