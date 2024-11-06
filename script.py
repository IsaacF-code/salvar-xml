import os
import zipfile
from datetime import datetime
from tqdm import tqdm

# Diretório onde os arquivos XML estão localizados
directory = 'D:\\CISS\\SAT\\CF-e\\Enviados'

# Diretório para salvar os arquivos compactados
output_directory = 'C:\\Users\\Caixa 6 - Loja 2\\Desktop\\ArquivosXML'

# Criar o diretório de saída, se não existir
os.makedirs(output_directory, exist_ok=True)

# Dicionário para armazenar arquivos por mês
files_by_month = {}

# Iterar sobre os arquivos no diretório
for filename in os.listdir(directory):
    if filename.endswith(".xml"):
        # Obter o caminho completo do arquivo
        file_path = os.path.join(directory, filename)
        
        # Obter a data de modificação do arquivo
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        month_year = file_date.strftime("%Y-%m")
        
        # Adicionar o arquivo ao dicionário correspondente ao mês
        if month_year not in files_by_month:
            files_by_month[month_year] = []
        files_by_month[month_year].append(file_path)

# Compactar os arquivos por mês
for month_year, files in tqdm(files_by_month.items(), desc="Compactando arquivos"):
    zip_filename = os.path.join(output_directory, f"CF-e {month_year} - Caixa.zip")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in tqdm(files, desc=f"{month_year}", leave=False):
            zipf.write(file, os.path.basename(file))

print("Arquivos XML foram compactados com sucesso por mês.")
