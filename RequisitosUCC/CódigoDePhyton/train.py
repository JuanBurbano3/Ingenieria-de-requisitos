import tkinter as tk
from tkinter import messagebox

class TrainTicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Compra de Boletos de Tren")

        self.origin_label = tk.Label(root, text="Origen:")
        self.origin_label.pack()

        self.destinations = ["Villa Nueva", "Castilla", "Vellice", "San Gregorio", "Madrid"]
        self.selected_origin = tk.StringVar()
        self.selected_destinations = []
        self.total_cost = 0

        self.origin_var = tk.StringVar()
        self.origin_dropdown = tk.OptionMenu(root, self.origin_var, *self.destinations, command=self.update_destination_options)
        self.origin_dropdown.pack()

        self.destination_label = tk.Label(root, text="Destino:")
        self.destination_label.pack()

        self.destination_var = tk.StringVar()
        self.destination_dropdown = tk.OptionMenu(root, self.destination_var, "")
        self.destination_dropdown.pack()

        self.add_button = tk.Button(root, text="Agregar Destino", command=self.add_destination)
        self.add_button.pack()

        self.clear_button = tk.Button(root, text="Limpiar Formulario", command=self.clear_form)
        self.clear_button.pack()

        self.total_label = tk.Label(root, text="Costo Total: $0")
        self.total_label.pack()

        self.continue_button = tk.Button(root, text="Continuar con el Pago", command=self.process_payment)
        self.continue_button.pack()

        self.cart_button = tk.Button(root, text="Carrito de Compras", command=self.show_cart)
        self.cart_button.pack()

    def update_destination_options(self, selected_origin):
        self.selected_origin.set(selected_origin)
        self.destination_var.set("")
        self.destination_dropdown['menu'].delete(0, 'end')

        for destination in self.destinations:
            if destination != selected_origin:
                self.destination_dropdown['menu'].add_command(label=destination, command=lambda dest=destination: self.destination_var.set(dest))

    def add_destination(self):
        destination = self.destination_var.get()
        if destination and destination not in self.selected_destinations and len(self.selected_destinations) < 5:
            self.selected_destinations.append(destination)
            self.total_cost += 10
            self.total_label.config(text=f"Costo Total: ${self.total_cost}")
            self.destination_var.set("")
        else:
            messagebox.showwarning("Error", "Debe seleccionar su destino")

    def clear_form(self):
        self.selected_destinations = []
        self.total_cost = 0
        self.total_label.config(text="Costo Total: $0")
        self.origin_var.set("")
        self.destination_var.set("")

    def process_payment(self):
        if self.selected_destinations:
            payment_window = tk.Toplevel(self.root)
            payment_window.title("Proceso de Pago")

            card_label = tk.Label(payment_window, text="Número de Tarjeta:")
            card_label.pack()

            card_entry = tk.Entry(payment_window)
            card_entry.pack()

            name_label = tk.Label(payment_window, text="Titular de la Tarjeta:")
            name_label.pack()

            name_entry = tk.Entry(payment_window)
            name_entry.pack()

            payment_button = tk.Button(payment_window, text="Realizar Pago", command=self.show_payment_success)
            payment_button.pack()
        else:
            messagebox.showwarning("Error", "Debe seleccionar al menos un destino antes de continuar con el pago.")

    def show_payment_success(self):
        messagebox.showinfo("Pago Exitoso", "El pago se realizó exitosamente.")

    def show_cart(self):
        if self.selected_destinations:
            cart_message = "Destinos en el Carrito:\n"
            for destination in self.selected_destinations:
                cart_message += f"- {destination}\n"
            messagebox.showinfo("Carrito de Compras", cart_message)
        else:
            messagebox.showinfo("Carrito de Compras", "El carrito de compras está vacío.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainTicketApp(root)
    root.mainloop()
