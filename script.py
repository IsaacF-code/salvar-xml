import os
import zipfile
from datetime import datetime
from tqdm import tqdm
import socket

# Mapeamento do penúltimo número do IP para o nome da Loja
location_map = {
    '0': 'Matriz',
    '1': 'Coronel',
    '2': 'Areias',
    '3': 'São Pedro',
    '4': 'Orós',
    '5': 'Cariús',
    '6': 'Jucás'
}

# Função para obter o último número do IP Local
def get_ip_parts():
    ip_address = socket.gethostbyname(socket.gethostname())
    parts = ip_address.split('.')
    last_part = parts[-1][-1] # Último dígito do IP
    penultimate_part = parts[-2] # Penúltima parte do IP
    return last_part, location_map.get(penultimate_part, "Desconhecido")

# Diretório onde os arquivos XML estão localizados
directory = 'C:\\CISS\\SAT\\CF-e\\Enviados'

# Diretório para salvar os arquivos compactados
output_directory = 'C:\\ArquivosXML'

# Arquivo de log para armazenar a última data compactada por mês
log_file_path = os.path.join(output_directory, 'Datas da compactação.txt')

# Criar o diretório de saída, se não existir
os.makedirs(output_directory, exist_ok=True)

# Função para carregar o log com as últimas datas compactadas
def load_last_compacted_dates():
    if not os.path.exists(log_file_path):
        return {}
    with open(log_file_path, 'r') as log_file:
        return dict(line.strip().split(',') for line in log_file)

# Função para atualizar o log com a última data compactada
def update_last_compacted_dates(dates):
    with open(log_file_path, 'w') as log_file:
        for month_year, date in dates.items():
            log_file.write(f"{month_year},{date}\n")

# Carregar as últimas datas compactadas
last_compacted_dates = load_last_compacted_dates()

# Dicionário para armazenar arquivos por mês
files_by_month = {}

ip_last_part, store = get_ip_parts()

# Iterar sobre os arquivos no diretório
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # Obter o caminho completo do arquivo
        file_path = os.path.join(directory, filename)
        
        # Obter a data de modificação do arquivo
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        month_year = file_date.strftime("%Y-%m")
        
        # Verificar se o arquivo é mais recente que o último compactado
        last_date_str = last_compacted_dates.get(month_year)
        last_date = datetime.strptime(last_date_str, "%Y-%m-%d %H:%M:%S") if last_date_str else None
        if not last_date or file_date > last_date:
            # Adicionar o arquivo ao dicionário correspondente ao mês
            if month_year not in files_by_month:
                files_by_month[month_year] = []
            files_by_month[month_year].append((file_path, file_date))

# Compactar os arquivos por mês
new_last_dates = {}
for month_year, files in tqdm(files_by_month.items(), desc="Compactando arquivos"):
    zip_filename = os.path.join(output_directory, f"CF-e {month_year} - Caixa {ip_last_part} - {store}.zip")
    with zipfile.ZipFile(zip_filename, 'a', zipfile.ZIP_DEFLATED) as zipf:
        for file_path, file_date in tqdm(files, desc=f"{month_year}", leave=False):
            zipf.write(file_path, os.path.basename(file_path))
            # Atualizar a última data compactada para o mês atual
            if month_year not in new_last_dates or file_date > new_last_dates[month_year]:
                new_last_dates[month_year] = file_date

# Atualizar o arquivo de log com as novas datas compactadas
update_last_compacted_dates({k: v.strftime("%Y-%m-%d %H:%M:%S") for k, v in new_last_dates.items()})

print("Arquivos XML foram compactados com sucesso por mês.")
