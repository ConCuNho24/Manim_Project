from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 14
config.frame_height = 7.875


def foot_of_perpendicular(P, X, Y):
    XY = Y - X
    t = np.dot(P - X, XY) / np.dot(XY, XY)
    return X + t * XY


def line_intersection(P1, P2, Q1, Q2):
    x1, y1 = P1[:2]
    x2, y2 = P2[:2]
    x3, y3 = Q1[:2]
    x4, y4 = Q2[:2]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if abs(denominator) < 1e-8:
        return np.array([0, 0, 0])

    px = (
        (x1 * y2 - y1 * x2) * (x3 - x4)
        - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denominator

    py = (
        (x1 * y2 - y1 * x2) * (y3 - y4)
        - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denominator

    return np.array([px, py, 0])


def circumcenter(A, B, C):
    x1, y1 = A[:2]
    x2, y2 = B[:2]
    x3, y3 = C[:2]

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    if abs(d) < 1e-8:
        return np.array([0, 0, 0])

    ux = (
        (x1**2 + y1**2) * (y2 - y3)
        + (x2**2 + y2**2) * (y3 - y1)
        + (x3**2 + y3**2) * (y1 - y2)
    ) / d

    uy = (
        (x1**2 + y1**2) * (x3 - x2)
        + (x2**2 + y2**2) * (x1 - x3)
        + (x3**2 + y3**2) * (x2 - x1)
    ) / d

    return np.array([ux, uy, 0])


class HinhAmsProject(Scene):
    def construct(self):
        # =============================
        # THIẾT LẬP CHUNG
        # =============================
        scale_factor = 0.7
        shift_vec = UP * 0.2

        main_stroke = 2
        thin_stroke = 1.6
        circle_stroke = 1.6

        # =============================
        # TAM GIÁC ABC
        # =============================
        A_pos = np.array([-1.3, 1.8, 0]) * scale_factor + shift_vec
        B_pos = np.array([-2.0, -2.0, 0]) * scale_factor + shift_vec
        C_pos = np.array([2.5, -2.0, 0]) * scale_factor + shift_vec

        A = Dot(A_pos, color=BLUE, radius=0.05)
        B = Dot(B_pos, color=BLUE, radius=0.05)
        C = Dot(C_pos, color=BLUE, radius=0.05)

        labelA = MathTex("A", font_size=20).next_to(A, UP, buff=0.1)
        labelB = MathTex("B", font_size=20).next_to(B, DOWN, buff=0.1)
        labelC = MathTex("C", font_size=20).next_to(C, RIGHT, buff=0.1)

        triangle = Polygon(
            A_pos,
            B_pos,
            C_pos,
            color=BLUE,
            stroke_width=main_stroke
        )

        self.play(Create(triangle))
        self.play(FadeIn(A, B, C), FadeIn(labelA, labelB, labelC))
        self.wait(0.5)

        # =============================
        # TÍNH CHÂN ĐƯỜNG CAO
        # =============================
        D_pos = foot_of_perpendicular(A_pos, B_pos, C_pos)  # D trên BC
        E_pos = foot_of_perpendicular(B_pos, A_pos, C_pos)  # E trên AC
        F_pos = foot_of_perpendicular(C_pos, A_pos, B_pos)  # F trên AB

        # =============================
        # VẼ ĐƯỜNG CAO AD
        # =============================
        AD_line = Line(A_pos, D_pos, color=ORANGE, stroke_width=thin_stroke)
        D = Dot(D_pos, color=WHITE, radius=0.04)
        labelD = MathTex("D", font_size=16).next_to(D, DOWN, buff=0.1)

        self.play(Create(AD_line))
        self.play(FadeIn(D), FadeIn(labelD))
        self.wait(0.3)

        # =============================
        # VẼ ĐƯỜNG CAO BE
        # =============================
        BE_line = Line(B_pos, E_pos, color=GREEN, stroke_width=thin_stroke)
        E = Dot(E_pos, color=GREEN, radius=0.04)
        labelE = MathTex("E", font_size=16).next_to(E, RIGHT, buff=0.1)

        self.play(Create(BE_line))
        self.play(FadeIn(E), FadeIn(labelE))
        self.wait(0.3)

        # =============================
        # VẼ ĐƯỜNG CAO CF
        # =============================
        CF_line = Line(C_pos, F_pos, color=RED, stroke_width=thin_stroke)
        F = Dot(F_pos, color=RED, radius=0.04)
        labelF = MathTex("F", font_size=16).next_to(F, LEFT, buff=0.1)

        self.play(Create(CF_line))
        self.play(FadeIn(F), FadeIn(labelF))
        self.wait(0.3)

        # =============================
        # TRỰC TÂM H
        # =============================
        H_pos = line_intersection(A_pos, D_pos, B_pos, E_pos)

        H = Dot(H_pos, color=YELLOW, radius=0.05)
        labelH = MathTex("H", font_size=20).next_to(H, DOWN + RIGHT, buff=0.1)

        self.play(FadeIn(H), FadeIn(labelH))
        self.wait(0.4)

        # =============================
        # ĐÁNH DẤU GÓC VUÔNG TẠI D, E, F
        # =============================
        right_angle_D = RightAngle(
            Line(D_pos, A_pos),
            Line(D_pos, C_pos),
            length=0.14,
            color=WHITE,
            stroke_width=1.4
        )

        right_angle_E = RightAngle(
            Line(E_pos, B_pos),
            Line(E_pos, C_pos),
            length=0.14,
            color=WHITE,
            stroke_width=1.4
        )

        right_angle_F = RightAngle(
            Line(F_pos, C_pos),
            Line(F_pos, A_pos),
            length=0.14,
            color=WHITE,
            stroke_width=1.4
        )

        self.play(Create(right_angle_D))
        self.play(Create(right_angle_E))
        self.play(Create(right_angle_F))
        self.wait(0.6)

        # =============================
        # ĐƯỜNG TRÒN NGOẠI TIẾP
        # =============================
        O_pos = circumcenter(A_pos, B_pos, C_pos)
        radius = np.linalg.norm(A_pos - O_pos)

        circumcircle = Circle(
            radius=radius,
            color=WHITE,
            stroke_width=circle_stroke
        ).move_to(O_pos)

        self.play(Create(circumcircle))
        self.wait(0.3)

        # =============================
        # QUA A KẺ ĐƯỜNG THẲNG SONG SONG BC
        # TỪ A QUA BÊN PHẢI CẮT ĐƯỜNG TRÒN TẠI K
        # =============================
        yA = A_pos[1]
        dx = np.sqrt(max(radius**2 - (yA - O_pos[1])**2, 0))
        K_pos = np.array([O_pos[0] + dx, yA, 0])

        AK_line = Line(A_pos, K_pos, color=YELLOW, stroke_width=thin_stroke)
        K = Dot(K_pos, color=YELLOW, radius=0.05)
        labelK = MathTex("K", font_size=18).next_to(K, RIGHT, buff=0.08)

        self.play(Create(AK_line))
        self.play(FadeIn(K), FadeIn(labelK))
        self.wait(0.4)

        # =============================
        # M LÀ TRUNG ĐIỂM BC
        # =============================
        M_pos = (B_pos + C_pos) / 2
        M = Dot(M_pos, color=TEAL, radius=0.05)
        labelM = MathTex("M", font_size=18).next_to(M, DOWN, buff=0.08)

        self.play(FadeIn(M), FadeIn(labelM))
        self.wait(0.3)

        # =============================
        # N ĐỐI XỨNG CỦA M QUA D
        # =============================
        N_pos = 2 * D_pos - M_pos
        N = Dot(N_pos, color=PURPLE, radius=0.05)
        labelN = MathTex("N", font_size=18).next_to(N, DOWN + LEFT, buff=0.08)

        self.play(FadeIn(N), FadeIn(labelN))
        self.wait(0.3)

        # =============================
        # NỐI NB, NA, MK
        # =============================
        NB_line = Line(N_pos, B_pos, color=PURPLE, stroke_width=thin_stroke)
        NA_line = Line(N_pos, A_pos, color=PURPLE, stroke_width=thin_stroke)
        MK_line = Line(M_pos, K_pos, color=TEAL, stroke_width=thin_stroke)

        self.play(Create(NB_line))
        self.play(Create(NA_line))
        self.play(Create(MK_line))
        self.wait(0.8)