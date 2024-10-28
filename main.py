from PIL import Image, ImageDraw, ImageFont
import qrcode
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib
import os

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def add_text_to_image(image, text, position, font_path="arial.ttf", font_size=50):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill="black")
    return image

def create_card(username, password, custom_text):
    # Carregar imagem base do diretório
    image_path = "crachamodelo.jpg"
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Imagem '{image_path}' não encontrada.")
        return None

    width, height = image.size

    # Gerar hash SHA256 da senha
    hashed_data = hashlib.sha256(password.encode()).hexdigest().upper()

    # Montar frase específica para o QR Code
    qr_data = f'{{"usuario":"{username}","senha":"{hashed_data}"}}'

    # Gerar QR Code com os dados
    qr_code = generate_qr_code(qr_data)
    qr_code = qr_code.resize((500, 500))  # Redimensionar QR Code se necessário

    # Inserir QR Code em uma posição relativa abaixo do centro
    qr_width, qr_height = qr_code.size
    qr_position = ((width - qr_width) // 2, int((height - qr_height) * 0.9))  # 90% da altura para posicionar um pouco abaixo do centro
    image.paste(qr_code, qr_position)

    # Adicionar texto centralizado acima do QR Code
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 50)  # Atualizar para o tamanho de fonte usado
    except IOError:
        font = ImageFont.load_default()
    text_width, text_height = draw.textbbox((0, 0), custom_text, font=font)[2:]  # Usar textbbox para obter o tamanho do texto
    text_position = ((width - text_width) // 2, qr_position[1] - text_height - 40)  # 20 pixels acima do QR Code
    add_text_to_image(image, custom_text, position=text_position, font_size=50)  # Passar o tamanho da fonte atualizado

    # Salvar dados em arquivo txt
    save_text_data(username, custom_text, qr_data)

    return image

def save_text_data(username, custom_text, qr_data):
    with open("crachas_info.txt", "a") as file:
        file.write(f"Usuário: {username}\nTexto: {custom_text}\nQR Code Data: {qr_data}\n\n")

def save_image(image, username):
    if image:
        save_path = f"{username}.jpg"
        image.save(save_path)
        image.show()
        messagebox.showinfo("Sucesso", f"Imagem salva como '{save_path}'")
    else:
        messagebox.showerror("Erro", "Falha ao salvar a imagem.")

def main():
    # Interface gráfica sofisticada
    def generate_card():
        username = entry_username.get()
        password = entry_password.get()
        custom_text = entry_text.get()

        if not username or not password:
            messagebox.showerror("Erro", "Por favor, insira o nome do usuário e a senha.")
            return

        card_image = create_card(username, password, custom_text)
        save_image(card_image, username)

    root = tk.Tk()
    root.title("Gerador de Crachá")
    root.geometry("400x300")
    root.resizable(False, False)

    # Widgets da interface
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Nome do Usuário:").grid(column=0, row=0, sticky=tk.W, pady=5)
    entry_username = ttk.Entry(frame, width=30)
    entry_username.grid(column=1, row=0, pady=5)

    ttk.Label(frame, text="Senha (6-8 dígitos):").grid(column=0, row=1, sticky=tk.W, pady=5)
    entry_password = ttk.Entry(frame, width=30)
    entry_password.grid(column=1, row=1, pady=5)

    ttk.Label(frame, text="Texto para o crachá:").grid(column=0, row=2, sticky=tk.W, pady=5)
    entry_text = ttk.Entry(frame, width=30)
    entry_text.grid(column=1, row=2, pady=5)

    generate_button = ttk.Button(frame, text="Gerar Crachá", command=generate_card)
    generate_button.grid(column=0, row=3, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
