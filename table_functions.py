import customtkinter as ctk
from dbFunc import fetch_all_students_with_grades, fetch_approved_students, fetch_failed_students

def create_table_header(table_frame):
    """Create table headers"""
    headers = ["ID", "Nome", "Nota 1", "Nota 2", "Média", "Status"]
    header_colors = ["#404040"] * 6
    
    for col, (header, color) in enumerate(zip(headers, header_colors)):
        header_label = ctk.CTkLabel(
            table_frame, 
            text=header, 
            fg_color=color,
            text_color="white",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=5
        )
        header_label.grid(row=0, column=col, padx=2, pady=2, sticky="ew")

def populate_table(table_frame, data_type="all"):
    """Populate the table with student data based on type"""
    # Clear existing data (except header)
    for widget in table_frame.winfo_children():
        if int(widget.grid_info()["row"]) > 0:  # Keep header row (row 0)
            widget.destroy()
    
    students_data = []
    
    if data_type == "all":
        students_data = fetch_all_students_with_grades()
    elif data_type == "approved":
        students_data = fetch_approved_students()
    elif data_type == "failed":
        students_data = fetch_failed_students()
    
    if students_data:
        for idx, student in enumerate(students_data, start=1):
            student_id = student.get("id", "N/A")
            nome = student.get("nome", "N/A")
            nota1 = student.get("nota1", "N/A")
            nota2 = student.get("nota2", "N/A")
            media = student.get("media", "N/A")
            
            # Determine status and colors
            if media != "N/A":
                try:
                    media_float = float(media)
                    status = "Aprovado" if media_float >= 7.0 else "Reprovado"
                    
                    # Set colors based on status
                    if status == "Aprovado":
                        row_color = "#2d5a3d"  # Dark green
                        text_color = "#90EE90"  # Light green text
                    else:
                        row_color = "#5a2d2d"  # Dark red
                        text_color = "#FFB6C1"  # Light red text
                
                    media_display = f"{media_float:.1f}"
                except (ValueError, TypeError):
                    status = "N/A"
                    row_color = "#404040"  # Gray
                    text_color = "#D3D3D3"  # Light gray text
                    media_display = str(media)
            else:
                status = "Sem Notas"
                row_color = "#404040"  # Gray
                text_color = "#D3D3D3"  # Light gray text
                media_display = "N/A"

            # Create row data
            row_data = [
                str(student_id),
                str(nome),
                str(nota1) if nota1 != "N/A" else "N/A",
                str(nota2) if nota2 != "N/A" else "N/A",
                media_display,
                status
            ]

            # Create labels for each column
            for col, data in enumerate(row_data):
                cell_label = ctk.CTkLabel(
                    table_frame,
                    text=data,
                    fg_color=row_color,
                    text_color=text_color,
                    font=ctk.CTkFont(size=11),
                    corner_radius=3
                )
                cell_label.grid(row=idx, column=col, padx=1, pady=1, sticky="ew")
    else:
        # No data message
        no_data_label = ctk.CTkLabel(
            table_frame,
            text="Nenhum dado encontrado",
            fg_color="#404040",
            text_color="white",
            font=ctk.CTkFont(size=12)
        )
        no_data_label.grid(row=1, column=0, columnspan=6, padx=10, pady=20, sticky="ew")

def setup_table_frame_columns(table_frame):
    """Configure table frame columns with appropriate weights and sizes"""
    table_frame.grid_columnconfigure(0, weight=1, minsize=50)   # ID
    table_frame.grid_columnconfigure(1, weight=3, minsize=200)  # Nome
    table_frame.grid_columnconfigure(2, weight=1, minsize=80)   # Nota 1
    table_frame.grid_columnconfigure(3, weight=1, minsize=80)   # Nota 2
    table_frame.grid_columnconfigure(4, weight=1, minsize=80)   # Média
    table_frame.grid_columnconfigure(5, weight=1, minsize=100)  # Status