import tkinter as tk
import random

# Configuration de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Pong")
largeur, hauteur = 800, 600
canvas = tk.Canvas(fenetre, width=largeur, height=hauteur, bg="black")
canvas.pack()

# Variables de la balle
ball_x, ball_y = largeur // 2, hauteur // 2
ball_x += random.randint(-200, 250)
ball_y += random.randint(-200, 250)
ball_dx, ball_dy = random.choice([5, -5]), random.choice([5, -5])
ball_radius = 10

# Variables des raquettes
raquette_largeur, raquette_hauteur = 10, 100
raquette_vitesse = 20
raquette_gauche_y = hauteur // 2 - raquette_hauteur // 2
raquette_droite_y = hauteur // 2 - raquette_hauteur // 2

# Variables pour le score
score_gauche = 0
score_droite = 0

# Dessiner les éléments du jeu
ball = canvas.create_oval(ball_x - ball_radius, ball_y - ball_radius, ball_x + ball_radius, ball_y + ball_radius, fill="white")
raquette_gauche = canvas.create_rectangle(0, raquette_gauche_y, raquette_largeur, raquette_gauche_y + raquette_hauteur, fill="white")
raquette_droite = canvas.create_rectangle(largeur - raquette_largeur, raquette_droite_y, largeur, raquette_droite_y + raquette_hauteur, fill="white")

# Commandes
commandes = {
    "gauche": {"haut": "z", "bas": "s"},
    "droite": {"haut": "Up", "bas": "Down"}
}

touches_pressees = {
    "gauche": {"haut": False, "bas": False},
    "droite": {"haut": False, "bas": False}
}

def mouvement_raquette_gauche():
    global raquette_gauche_y
    if touches_pressees["gauche"]["haut"] and raquette_gauche_y > 0:
        raquette_gauche_y -= raquette_vitesse
    if touches_pressees["gauche"]["bas"] and raquette_gauche_y < hauteur - raquette_hauteur:
        raquette_gauche_y += raquette_vitesse
    canvas.coords(raquette_gauche, 0, raquette_gauche_y, raquette_largeur, raquette_gauche_y + raquette_hauteur)

def mouvement_raquette_droite():
    global raquette_droite_y
    if touches_pressees["droite"]["haut"] and raquette_droite_y > 0:
        raquette_droite_y -= raquette_vitesse
    if touches_pressees["droite"]["bas"] and raquette_droite_y < hauteur - raquette_hauteur:
        raquette_droite_y += raquette_vitesse
    canvas.coords(raquette_droite, largeur - raquette_largeur, raquette_droite_y, largeur, raquette_droite_y + raquette_hauteur)

def gerer_touche(event, pression):
    if event.keysym == commandes["gauche"]["haut"]:
        touches_pressees["gauche"]["haut"] = pression
    elif event.keysym == commandes["gauche"]["bas"]:
        touches_pressees["gauche"]["bas"] = pression
    elif event.keysym == commandes["droite"]["haut"]:
        touches_pressees["droite"]["haut"] = pression
    elif event.keysym == commandes["droite"]["bas"]:
        touches_pressees["droite"]["bas"] = pression

fenetre.bind("<KeyPress>", lambda e: gerer_touche(e, True))
fenetre.bind("<KeyRelease>", lambda e: gerer_touche(e, False))

score_text = canvas.create_text(largeur // 2, 20, text=f"{score_gauche} - {score_droite}", font=("Arial", 30), fill="white")

def mettre_a_jour_score():
    canvas.itemconfig(score_text, text=f"{score_gauche} - {score_droite}")

def lancer_mini_jeu():
    mini_fenetre = tk.Toplevel()
    mini_fenetre.title("Mini-Jeu")
    mini_fenetre.geometry("400x300")
    barre_gauche = tk.IntVar(value=0)
    barre_droite = tk.IntVar(value=0)

    def clic_gauche():
        if barre_gauche.get() < 50:
            barre_gauche.set(barre_gauche.get() + 1)
        verifier_vainqueur()

    def clic_droite():
        if barre_droite.get() < 50:
            barre_droite.set(barre_droite.get() + 1)
        verifier_vainqueur()

    def verifier_vainqueur():
        global score_gauche, score_droite
        if barre_gauche.get() >= 50:
            score_gauche += 5
            mettre_a_jour_score()
            mini_fenetre.destroy()
        elif barre_droite.get() >= 50:
            score_droite += 5
            mettre_a_jour_score()
            mini_fenetre.destroy()

    tk.Label(mini_fenetre, text="Cliquez rapidement !", font=("Arial", 16)).pack()
    tk.Button(mini_fenetre, text="Joueur Gauche", command=clic_gauche, bg="blue", fg="white").pack(side="left", expand=True, fill="both")
    tk.Button(mini_fenetre, text="Joueur Droite", command=clic_droite, bg="red", fg="white").pack(side="right", expand=True, fill="both")

def mouvement_balle():
    global ball_x, ball_y, ball_dx, ball_dy, score_gauche, score_droite
    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= hauteur:
        ball_dy *= -1

    if (ball_x - ball_radius <= raquette_largeur and raquette_gauche_y <= ball_y <= raquette_gauche_y + raquette_hauteur) or (ball_x + ball_radius >= largeur - raquette_largeur and raquette_droite_y <= ball_y <= raquette_droite_y + raquette_hauteur):
        ball_dx *= -1

    if ball_x - ball_radius <= 0:
        score_droite += 1
        mettre_a_jour_score()
        if score_gauche == score_droite:
            lancer_mini_jeu()
        ball_x, ball_y = largeur // 2, hauteur // 2
        ball_dx, ball_dy = random.choice([5, -5]), random.choice([5, -5])

    elif ball_x + ball_radius >= largeur:
        score_gauche += 1
        mettre_a_jour_score()
        if score_gauche == score_droite:
            lancer_mini_jeu()
        ball_x, ball_y = largeur // 2, hauteur // 2
        ball_dx, ball_dy = random.choice([5, -5]), random.choice([5, -5])

    canvas.coords(ball, ball_x - ball_radius, ball_y - ball_radius, ball_x + ball_radius, ball_y + ball_radius)
    mouvement_raquette_gauche()
    mouvement_raquette_droite()
    fenetre.after(50, mouvement_balle)

mouvement_balle()
fenetre.mainloop()
