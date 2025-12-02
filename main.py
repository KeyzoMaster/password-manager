import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame
import pyperclip
from manager import Manager
from util import Password
from password import check_strength


class PasswordManagerApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Gestionnaire de mots de passe")
        self.geometry("1280x720")
        self.manager = Manager()
        self.show_login_frame()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.clear_window()

        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        ttk.Label(container, text="Connextion", font=("Helvetica", 24, "bold")).pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(container, text="Nom d'utilisateur").pack(fill=X, pady=(10, 0))
        ttk.Entry(container, textvariable=self.username_var).pack(fill=X, pady=5)

        ttk.Label(container, text="Mot de passe").pack(fill=X, pady=(10, 0))
        ttk.Entry(container, textvariable=self.password_var, show="*").pack(fill=X, pady=5)

        ttk.Button(container, text="Se connecter", bootstyle=PRIMARY, command=self.login).pack(fill=X, pady=20)

        ttk.Button(container, text="S'enregister", bootstyle=LINK, command=self.show_register_frame).pack()

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return

        success = self.manager.login(username, password)
        if success:
            self.show_dashboard_frame()
        else:
            messagebox.showerror("Erreur", "Utilisateur inexistant ou mot de passe incorrect")


    def show_register_frame(self):
        self.clear_window()

        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor=CENTER)

        ttk.Label(container, text="Register", font=("Helvetica", 24, "bold")).pack(pady=20)

        self.reg_username = tk.StringVar()
        self.reg_password = tk.StringVar()
        self.reg_confirm = tk.StringVar()

        ttk.Label(container, text="Nom d'utilisateur").pack(fill=X)
        ttk.Entry(container, textvariable=self.reg_username).pack(fill=X, pady=5)

        ttk.Label(container, text="Mot de passe").pack(fill=X, pady=(10, 0))
        ent_pw = ttk.Entry(container, textvariable=self.reg_password, show="*")
        ent_pw.pack(fill=X, pady=5)
        # Live strength check binding
        ent_pw.bind("<KeyRelease>", self.update_strength_meter)

        self.strength_label = ttk.Label(container, text="", font=("Helvetica", 8))
        self.strength_label.pack(fill=X)

        ttk.Label(container, text="Confirmez le mot de passe").pack(fill=X, pady=(10, 0))
        ttk.Entry(container, textvariable=self.reg_confirm, show="*").pack(fill=X, pady=5)

        ttk.Button(container, text="S'enregistrer", bootstyle=SUCCESS, command=self.perform_register).pack(fill=X,
                                                                                                            pady=20)
        ttk.Button(container, text="Retour à la page de connexion", bootstyle=SECONDARY, command=self.show_login_frame).pack(fill=X)

    def update_strength_meter(self,event):
        pw = self.reg_password.get()
        if not pw:
            self.strength_label.config(text="", bootstyle=DEFAULT)
            return
        score, msg = check_strength(pw)

        if score < 2:
            self.strength_label.config(text=msg, bootstyle=DANGER)
        elif score < 4:
            self.strength_label.config(text=msg, bootstyle=WARNING)
        else:
            self.strength_label.config(text=msg, bootstyle=SUCCESS)

    def perform_register(self):
        user = self.reg_username.get().strip()
        pw = self.reg_password.get().strip()
        confirm = self.reg_confirm.get().strip()

        if pw != confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return

        score, _ = check_strength(pw)
        if score < 3:
            messagebox.showwarning("Danger", "Votre mot de passe est trop faible")

        try:
            self.manager.create_user(user, pw)
            messagebox.showinfo("Succès", "Compte créé avec succès !")
            self.show_login_frame()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de la création de l'utilisateur.\n{e}")


    def show_dashboard_frame(self):
        self.clear_window()

        header = ttk.Frame(self, padding=10, bootstyle=PRIMARY)
        header.pack(fill=X)

        ttk.Label(header, text=f"Bienvenue, {self.manager.user.username}", font=("Helvetica", 14, "bold"),
                  bootstyle="inverse-primary").pack(side=LEFT)
        ttk.Button(header, text="Se déconnecter", bootstyle="danger-outline", command=self.logout).pack(side=RIGHT)

        add_frame = ttk.Labelframe(self, text="Ajouter un nouveau mot de passe", padding=15)
        add_frame.pack(fill=X, padx=20, pady=10)

        # Layout for Add Form
        f1 = ttk.Frame(add_frame)
        f1.pack(fill=X)

        ttk.Label(f1, text="Libellé").pack(side=LEFT, padx=(0, 5))
        self.new_label = ttk.Entry(f1, width=20)
        self.new_label.pack(side=LEFT, padx=(0, 15))

        ttk.Label(f1, text="Login/Email (Optionel)").pack(side=LEFT, padx=(0, 5))
        self.new_login = ttk.Entry(f1, width=20)
        self.new_login.pack(side=LEFT, padx=(0, 15))

        ttk.Label(f1, text="Mot de passe").pack(side=LEFT, padx=(0, 5))
        self.new_pw = ttk.Entry(f1, width=20)
        self.new_pw.pack(side=LEFT, padx=(0, 15))

        ttk.Button(f1, text="Ajouter", bootstyle=SUCCESS, command=self.add_password).pack(side=LEFT)

        # --- Password List Section ---
        list_container = ttk.Labelframe(self, text="Mes Mots de Passe", padding=15)
        list_container.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        # Scrollable area
        sf = ScrolledFrame(list_container, autohide=True)
        sf.pack(fill=BOTH, expand=True)

        # Headers
        header_row = ttk.Frame(sf)
        header_row.pack(fill=X, pady=5)
        ttk.Label(header_row, text="Libelle", font=("Helvetica", 10, "bold"), width=15).pack(side=LEFT, padx=5)
        ttk.Label(header_row, text="Login", font=("Helvetica", 10, "bold"), width=30).pack(side=LEFT, padx=5)
        ttk.Label(header_row, text="Mot de passe", font=("Helvetica", 10, "bold"), width=35).pack(side=LEFT, padx=5)
        ttk.Label(header_row, text="Actions", font=("Helvetica", 10, "bold")).pack(side=LEFT, padx=5)

        ttk.Separator(sf).pack(fill=X, pady=5)

        # Render Items
        if not self.manager.user.passwords:
            ttk.Label(sf, text="Aucun mot de passe n'a encore été enregistré").pack(pady=20)
        else:
            for pw_obj in self.manager.user.passwords:
                self.create_password_row(sf, pw_obj)

    def create_password_row(self, parent, pw_obj: Password):
        row = ttk.Frame(parent)
        row.pack(fill=X, pady=5)

        ttk.Label(row, text=pw_obj.label, width=15, anchor=W).pack(side=LEFT, padx=5)
        ttk.Label(row, text=pw_obj.login, width=20, anchor=W).pack(side=LEFT, padx=5)
        real_password = pw_obj.get_password()

        pw_entry = ttk.Entry(row, width=25, show="*")
        pw_entry.insert(0, real_password)
        pw_entry.config(state="readonly")
        pw_entry.pack(side=LEFT, padx=5)


        def toggle():
            if pw_entry.cget('show') == '*':
                pw_entry.config(show='')
                btn_eye.config(text="Masquer", bootstyle=SECONDARY)
            else:
                pw_entry.config(show='*')
                btn_eye.config(text="Afficher", bootstyle=INFO)

        btn_eye = ttk.Button(row, text="Afficher", bootstyle=INFO, width=10, command=toggle)
        btn_eye.pack(side=LEFT, padx=2)

        # Copy
        def copy():
            pyperclip.copy(real_password)
            ttk.Button(row, text="Copié!", bootstyle=SUCCESS, width=10).pack(side=LEFT, padx=2)
            self.after(1000, self.show_dashboard_frame)

        ttk.Button(row, text="Copier", bootstyle=DARK, width=6, command=copy).pack(side=LEFT, padx=2)

        # Edit
        ttk.Button(row, text="Modifier", bootstyle=WARNING, width=10,
                   command=lambda: self.edit_password_dialog(pw_obj)).pack(side=LEFT, padx=2)

        # Delete
        def delete():
            if messagebox.askyesno("Confirmation", f"Supprimer le mot de passe de {pw_obj.label}?"):
                self.manager.delete_password(pw_obj)
                self.show_dashboard_frame()

        ttk.Button(row, text="Supprimer", bootstyle=DANGER, width=10, command=delete).pack(side=LEFT, padx=2)

    def logout(self):
        self.manager.logout()
        self.show_login_frame()

    def add_password(self):
        label = self.new_label.get().strip()
        login = self.new_login.get().strip()
        pw = self.new_pw.get().strip()

        if not label or not pw:
            messagebox.showwarning("Données manquantes", "Le libellé et le mot de passe sont obligatoires.")
            return

        # Check strength before adding
        score, msg = check_strength(pw)
        if score < 3:
            if not messagebox.askyesno("Mot de passe faible", "Ajouter quand meme ?"):
                return

        try:
            # CLEANER: Calling the updated manager method
            self.manager.add_password(label, pw, login)
            self.show_dashboard_frame()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'ajout du mot de passe.\n{e}")

    def edit_password_dialog(self, pw_obj):
        top = ttk.Toplevel(self)
        top.title(f"Modifier {pw_obj.label}")
        top.geometry("300x200")

        ttk.Label(top, text="Nouveau mot de passe").pack(pady=10)
        new_var = tk.StringVar()
        ttk.Entry(top, textvariable=new_var).pack(pady=5)

        def save():
            new_pass = new_var.get().strip()
            if new_pass:
                self.manager.update_password(pw_obj.password_id, new_pass)
                top.destroy()
                self.show_dashboard_frame()
            else:
                messagebox.showwarning("Erreur", "Le mot de passe ne peut etre vide")

        ttk.Button(top, text="Sauvegarder", bootstyle=SUCCESS, command=save).pack(pady=20)


if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()