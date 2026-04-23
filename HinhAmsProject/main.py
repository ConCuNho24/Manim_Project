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


def line_circle_second_intersection(P1, P2, O, r):
    """
    Tìm giao điểm thứ hai của đường thẳng P1P2 với đường tròn tâm O bán kính r.
    Giả sử P1 đang nằm trên đường tròn, trả về giao điểm còn lại.
    """
    d = P2 - P1
    f = P1 - O

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - r**2

    delta = b**2 - 4 * a * c
    if delta < 0:
        return np.array([0, 0, 0])

    sqrt_delta = np.sqrt(delta)

    t1 = (-b - sqrt_delta) / (2 * a)
    t2 = (-b + sqrt_delta) / (2 * a)

    # Vì P1 nằm trên đường tròn nên một nghiệm là gần 0
    # Nghiệm còn lại là giao điểm thứ hai
    if abs(t1) < abs(t2):
        t_other = t2
    else:
        t_other = t1

    return P1 + t_other * d

def second_intersection_line_circle_on_line(P1, P2, center, radius, known_point):
    """
    Tìm giao điểm thứ hai của đường thẳng P1P2 với đường tròn tâm center bán kính radius,
    biết known_point là một giao điểm đã biết trên đường tròn.
    """
    d = P2 - P1
    f = P1 - center

    a = np.dot(d, d)
    b = 2 * np.dot(f, d)
    c = np.dot(f, f) - radius**2

    delta = b**2 - 4 * a * c
    if delta < 0:
        return np.array([0, 0, 0])

    sqrt_delta = np.sqrt(delta)

    t1 = (-b - sqrt_delta) / (2 * a)
    t2 = (-b + sqrt_delta) / (2 * a)

    X1 = P1 + t1 * d
    X2 = P1 + t2 * d

    if np.linalg.norm(X1 - known_point) < np.linalg.norm(X2 - known_point):
        return X2
    else:
        return X1
    
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
        A_pos = np.array([-1.25, 1.2, 0]) * scale_factor + shift_vec
        B_pos = np.array([-2.0, -2.0, 0]) * scale_factor + shift_vec
        C_pos = np.array([2.5, -2.0, 0]) * scale_factor + shift_vec

        A = Dot(A_pos, color=BLUE, radius=0.05)
        B = Dot(B_pos, color=BLUE, radius=0.05)
        C = Dot(C_pos, color=BLUE, radius=0.05)

        labelA = MathTex("A", font_size=12).next_to(A, UP, buff=0.1)
        labelB = MathTex("B", font_size=12).next_to(B, DOWN, buff=0.1)
        labelC = MathTex("C", font_size=12).next_to(C, RIGHT, buff=0.1)

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
        D_pos = foot_of_perpendicular(A_pos, B_pos, C_pos)
        E_pos = foot_of_perpendicular(B_pos, A_pos, C_pos)
        F_pos = foot_of_perpendicular(C_pos, A_pos, B_pos)

        # =============================
        # VẼ ĐƯỜNG CAO AD
        # =============================
        AD_line = Line(A_pos, D_pos, color=ORANGE, stroke_width=thin_stroke)
        D = Dot(D_pos, color=WHITE, radius=0.04)
        labelD = MathTex("D", font_size=12).next_to(D, (DOWN + RIGHT) * 0.75, buff=0.1)

        self.play(Create(AD_line))
        self.play(FadeIn(D), FadeIn(labelD))
        self.wait(0.3)

        # =============================
        # VẼ ĐƯỜNG CAO BE
        # =============================
        BE_line = Line(B_pos, E_pos, color=GREEN, stroke_width=thin_stroke)
        E = Dot(E_pos, color=GREEN, radius=0.04)
        labelE = MathTex("E", font_size=12).next_to(E, RIGHT, buff=0.1)

        self.play(Create(BE_line))
        self.play(FadeIn(E), FadeIn(labelE))
        self.wait(0.3)

        # =============================
        # VẼ ĐƯỜNG CAO CF
        # =============================
        CF_line = Line(C_pos, F_pos, color=RED, stroke_width=thin_stroke)
        F = Dot(F_pos, color=RED, radius=0.04)
        labelF = MathTex("F", font_size=12).next_to(F, UP*1.1, buff=0.1)

        self.play(Create(CF_line))
        self.play(FadeIn(F), FadeIn(labelF))
        self.wait(0.3)

        # =============================
        # TRỰC TÂM H
        # =============================
        H_pos = line_intersection(A_pos, D_pos, B_pos, E_pos)

        H = Dot(H_pos, color=YELLOW, radius=0.05)
        labelH = MathTex("H", font_size=12).next_to(H, DOWN + RIGHT, buff=0.1)

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
        labelK = MathTex("K", font_size=12).next_to(K, RIGHT, buff=0.08)

        self.play(Create(AK_line))
        self.play(FadeIn(K), FadeIn(labelK))
        self.wait(0.4)

        # =============================
        # M LÀ TRUNG ĐIỂM BC
        # =============================
        M_pos = (B_pos + C_pos) / 2
        M = Dot(M_pos, color=TEAL, radius=0.05)
        labelM = MathTex("M", font_size=12).next_to(M, DOWN, buff=0.08)

        self.play(FadeIn(M), FadeIn(labelM))
        self.wait(0.3)

        # =============================
        # N ĐỐI XỨNG CỦA M QUA D
        # =============================
        N_pos = 2 * D_pos - M_pos
        N = Dot(N_pos, color=PURPLE, radius=0.05)
        labelN = MathTex("N", font_size=12).next_to(N, DOWN + LEFT, buff=0.08)

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
        self.wait(0.5)

        # =============================
        # HIGHLIGHT TỨ GIÁC AKMN
        # =============================
        quad_AKMN = Polygon(
            A_pos, K_pos, M_pos, N_pos,
            color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.18
        )

        self.play(FadeIn(quad_AKMN))
        self.wait(0.6)
        self.play(FadeOut(quad_AKMN))
        self.wait(0.2)

        # =============================
        # KÉO DÀI AD CẮT ĐƯỜNG TRÒN NGOẠI TIẾP TẠI P
        # =============================
        P_pos = line_circle_second_intersection(A_pos, D_pos, O_pos, radius)

        AP_line = Line(A_pos, P_pos, color=ORANGE, stroke_width=thin_stroke)
        P = Dot(P_pos, color=ORANGE, radius=0.05)
        labelP = MathTex("P", font_size=12).next_to(P, DOWN, buff=0.08)

        self.play(Transform(AD_line, AP_line))
        self.play(FadeIn(P), FadeIn(labelP))
        self.wait(0.8)
        # =============================
        # VẼ EF
        # =============================
        EF_line = Line(E_pos, F_pos, color=WHITE, stroke_width=thin_stroke)
        self.play(Create(EF_line))
        self.wait(0.3)

        # =============================
        # I LÀ TRUNG ĐIỂM EF
        # =============================
        I_pos = (E_pos + F_pos) / 2
        I = Dot(I_pos, color=TEAL, radius=0.05)
        labelI = MathTex("I", font_size=12).next_to(I, UP + RIGHT * 0.1, buff=0.08)

        self.play(FadeIn(I), FadeIn(labelI))
        self.wait(0.3)

        # =============================
        # DỰNG J:
        # J LÀ GIAO ĐIỂM THỨ 2 CỦA ĐƯỜNG THẲNG EF
        # VỚI ĐƯỜNG TRÒN TÂM H BÁN KÍNH HI
        # (KHÔNG HIỆN ĐƯỜNG TRÒN)
        # =============================
        HI_radius = np.linalg.norm(I_pos - H_pos)
        J_pos = second_intersection_line_circle_on_line(
            E_pos, F_pos, H_pos, HI_radius, I_pos
        )

        J = Dot(J_pos, color=MAROON, radius=0.05)
        labelJ = MathTex("J", font_size=12).next_to(J, UP, buff=0.08)

        self.play(FadeIn(J), FadeIn(labelJ))
        self.wait(0.3)

        # =============================
        # NỐI JF (CÙNG MÀU VỚI EF)
        # =============================
        JF_line = Line(J_pos, F_pos, color=WHITE, stroke_width=thin_stroke)
        self.play(Create(JF_line))
        self.wait(0.3)

        # =============================
        # NỐI HI VÀ HJ
        # =============================
        HI_line = Line(H_pos, I_pos, color=WHITE, stroke_width=thin_stroke)
        HJ_line = Line(H_pos, J_pos, color=WHITE, stroke_width=thin_stroke)

        self.play(Create(HI_line))
        self.play(Create(HJ_line))
        self.wait(0.6)
                # =============================
        # NỐI JA, NK, BK (RẤT MẢNH - CÙNG LÚC)
        # =============================
        # ultra_thin = 0.9  # có thể giảm xuống 0.7 nếu muốn mảnh hơn nữa

        JA_line = Line(A_pos, J_pos, color=GREY, stroke_width=thin_stroke)
        NK_line = Line(N_pos, K_pos, color=GREY, stroke_width=thin_stroke)
        BK_line = Line(B_pos, K_pos, color=GREY, stroke_width=thin_stroke)

        self.play(
            Create(JA_line),
            Create(NK_line),
            Create(BK_line),
        )
        self.wait(0.6)

        KC_line = Line(K_pos, C_pos, color=GREY, stroke_width=thin_stroke)
        self.play(
            Create(KC_line)
        )
        self.wait(0.6)

        # =============================
        # HIGHLIGHT TAM GIÁC AEF VÀ KBC
        # =============================
        tri_AEF = Polygon(
            A_pos, E_pos, F_pos,
            color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.2
        )

        tri_KBC = Polygon(
            K_pos, B_pos, C_pos,
            color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.2
        )

        self.play(
            FadeIn(tri_AEF),
            FadeIn(tri_KBC)
        )
        self.wait(0.6)
        # =============================
        # NỐI AI
        # =============================
        AI_line = Line(A_pos, I_pos, color=TEAL, stroke_width=thin_stroke)
        self.play(Create(AI_line))
        self.wait(0.3)

        # =============================
        # HIGHLIGHT AI THEO KM
        # =============================
        highlight_color = TEAL

        AI_highlight = Line(A_pos, I_pos, color=highlight_color, stroke_width=3)
        KM_highlight = Line(K_pos, M_pos, color=highlight_color, stroke_width=3)

        self.play(
            Transform(AI_line, AI_highlight),
            Transform(MK_line, KM_highlight),
        )
        self.wait(0.6)

        # =============================
        # NỐI PB VÀ PC
        # =============================
        PB_line = Line(P_pos, B_pos, color=GREY, stroke_width=thin_stroke)
        PC_line = Line(P_pos, C_pos, color=GREY, stroke_width=thin_stroke)

        self.play(
            Create(PB_line),
            Create(PC_line)
        )
        self.wait(0.4)

        # =============================
        # HIGHLIGHT TAM GIÁC FHE VÀ BPC
        # =============================
        tri_FHE = Polygon(
            F_pos, H_pos, E_pos,
            color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.2
        )

        tri_BPC = Polygon(
            B_pos, P_pos, C_pos,
            color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.2
        )

        self.play(
            FadeIn(tri_FHE),
            FadeIn(tri_BPC)
        )
        self.wait(0.6)
        # =============================
        # NỐI PM VÀ PN
        # =============================
        PM_line = Line(P_pos, M_pos, color=GREY, stroke_width=thin_stroke)
        PN_line = Line(P_pos, N_pos, color=GREY, stroke_width=thin_stroke)

        self.play(
            Create(PM_line),
            Create(PN_line)
        )
        self.wait(0.3)

        # =============================
        # HIGHLIGHT HI, HJ, PM, PN (MÀU TÍM)
        # =============================
        highlight_color = PURPLE

        HI_highlight = Line(H_pos, I_pos, color=highlight_color, stroke_width=3)
        HJ_highlight = Line(H_pos, J_pos, color=highlight_color, stroke_width=3)
        PM_highlight = Line(P_pos, M_pos, color=highlight_color, stroke_width=3)
        PN_highlight = Line(P_pos, N_pos, color=highlight_color, stroke_width=3)

        # =============================
        # TAM GIÁC PMN VÀ HIJ (MÀU TÍM)
        # =============================
        tri_PMN = Polygon(
            P_pos, M_pos, N_pos,
            color=highlight_color,
            stroke_width=3,
            fill_color=highlight_color,
            fill_opacity=0.2
        )

        tri_HIJ = Polygon(
            H_pos, I_pos, J_pos,
            color=highlight_color,
            stroke_width=3,
            fill_color=highlight_color,
            fill_opacity=0.2
        )

        self.play(
            Transform(HI_line, HI_highlight),
            Transform(HJ_line, HJ_highlight),
            Transform(PM_line, PM_highlight),
            Transform(PN_line, PN_highlight),
            FadeIn(tri_PMN),
            FadeIn(tri_HIJ),
        )
        self.wait(0.8)
        # =============================
        # HIGHLIGHT N & J (POPUP + ĐỎ)
        # =============================
        self.play(
            N.animate.set_color(RED).scale(1.4),
            J.animate.set_color(RED).scale(1.4),
            run_time=0.3
        )
        self.play(
            N.animate.scale(1/1.4),
            J.animate.scale(1/1.4),
            run_time=0.2
        )

        # =============================
        # HIGHLIGHT B & F
        # =============================
        self.play(
            B.animate.set_color(RED).scale(1.4),
            F.animate.set_color(RED).scale(1.4),
            run_time=0.3
        )
        self.play(
            B.animate.scale(1/1.4),
            F.animate.scale(1/1.4),
            run_time=0.2
        )

        # =============================
        # HIGHLIGHT K & A
        # =============================
        self.play(
            K.animate.set_color(RED).scale(1.4),
            A.animate.set_color(RED).scale(1.4),
            run_time=0.3
        )
        self.play(
            K.animate.scale(1/1.4),
            A.animate.scale(1/1.4),
            run_time=0.2
        )

        self.wait(0.2)

        # =============================
        # HIGHLIGHT TAM GIÁC NBK VÀ JFA (XANH LÁ)
        # =============================
        tri_NBK = Polygon(
            N_pos, B_pos, K_pos,
            color=GREEN,
            stroke_width=3,
            fill_color=GREEN,
            fill_opacity=0.25
        )

        tri_JFA = Polygon(
            J_pos, F_pos, A_pos,
            color=GREEN,
            stroke_width=3,
            fill_color=GREEN,
            fill_opacity=0.25
        )

        self.play(
            FadeIn(tri_NBK),
            FadeIn(tri_JFA)
        )
        self.wait(0.8)