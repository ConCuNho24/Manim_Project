from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16


class Test(Scene):
    def construct(self):
        # =============================
        # TAM GIÁC ABC (BÊN TRÁI)
        # =============================
        A = LEFT * 3.25 + UP * 0.5
        B = LEFT * 4.0 + DOWN * 1.5
        C = LEFT * 2 + DOWN * 1.5

        triangle_ABC = Polygon(A, B, C, color=BLUE)

        label_A = Text("A", font_size=28).next_to(A, UP)
        label_B = Text("B", font_size=28).next_to(B, DOWN)
        label_C = Text("C", font_size=28).next_to(C, DOWN)

        # =============================
        # TAM GIÁC A'B'C' (BÊN PHẢI - ĐỒNG DẠNG, LỚN HƠN)
        # =============================
        scale_factor = 1.6

        A_p = RIGHT * 1.5 + UP * 1.5
        B_p = A_p + (B - A) * scale_factor
        C_p = A_p + (C - A) * scale_factor

        triangle_big = Polygon(A_p, B_p, C_p, color=YELLOW)

        label_Ap = Text("A'", font_size=28).next_to(A_p, UP)
        label_Bp = Text("B'", font_size=28).next_to(B_p, DOWN)
        label_Cp = Text("C'", font_size=28).next_to(C_p, DOWN)

        # =============================
        # HÀM TÍNH GIAO ĐIỂM CỦA PHÂN GIÁC TỪ A VỚI BC
        # ĐỊNH LÝ PHÂN GIÁC: BD/DC = AB/AC
        # =============================
        def angle_bisector_foot(PA, PB, PC):
            AB_len = np.linalg.norm(PB - PA)
            AC_len = np.linalg.norm(PC - PA)
            t = AB_len / (AB_len + AC_len)
            return PB + t * (PC - PB)

        D_pos = angle_bisector_foot(A, B, C)
        D_p_pos = angle_bisector_foot(A_p, B_p, C_p)

        D = Dot(D_pos, color=WHITE)
        D_p = Dot(D_p_pos, color=WHITE)

        label_D = Text("D", font_size=28).next_to(D, DOWN)
        label_Dp = Text("D'", font_size=28).next_to(D_p, DOWN)

        # =============================
        # PHÂN GIÁC AD, A'D'
        # =============================
        AD = Line(A, D_pos, color=WHITE)
        AD_p = Line(A_p, D_p_pos, color=WHITE)

        # =============================
        # HÀM TẠO CUNG ĐÁNH DẤU GÓC
        # num_arcs = 1 hoặc 2 để phân biệt kiểu ký hiệu nếu cần
        # Ở đây ta dùng cùng 1 kiểu cho các góc phân giác tương ứng
        # =============================
        def make_angle_marks(vertex, p1, p2, radius=0.35, color=WHITE, num_arcs=1, gap=0.08):
            u1 = p1 - vertex
            u2 = p2 - vertex

            a1 = np.arctan2(u1[1], u1[0])
            a2 = np.arctan2(u2[1], u2[0])

            diff = (a2 - a1) % (2 * np.pi)
            if diff > np.pi:
                a1, a2 = a2, a1
                diff = (a2 - a1) % (2 * np.pi)

            arcs = VGroup()
            for i in range(num_arcs):
                r = radius + i * gap
                arc = Arc(
                    radius=r,
                    start_angle=a1,
                    angle=diff,
                    arc_center=vertex,
                    color=color,
                    stroke_width=3
                )
                arcs.add(arc)
            return arcs

        # Góc BAD = DAC
        angle_BAD = make_angle_marks(A, B, D_pos, radius=0.30, color=GREEN)
        angle_DAC = make_angle_marks(A, D_pos, C, radius=0.4, color=GREEN)

        # Góc B'A'D' = D'A'C'
        angle_BpApDp = make_angle_marks(A_p, B_p, D_p_pos, radius=0.34, color=GREEN)
        angle_DpApCp = make_angle_marks(A_p, D_p_pos, C_p, radius=0.45, color=GREEN)

        # =============================
        # CÁC TAM GIÁC CẦN HIGHLIGHT
        # =============================
        tri_ADB = Polygon(A, D_pos, B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ApDpBp = Polygon(A_p, D_p_pos, B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)

        tri_ADC = Polygon(A, D_pos, C, stroke_width=0, fill_color=RED, fill_opacity=0)
        tri_ApDpCp = Polygon(A_p, D_p_pos, C_p, stroke_width=0, fill_color=RED, fill_opacity=0)

        group_ADB = VGroup(tri_ADB, tri_ApDpBp)
        group_ADC = VGroup(tri_ADC, tri_ApDpCp)

        popup_1 = MathTex(r"\triangle ADB \sim \triangle A'D'B'")
        popup_1.scale(0.9)
        popup_1.move_to((group_ADB[0].get_center() + group_ADB[1].get_center()) / 2 + DOWN * 4)

        popup_2 = MathTex(r"\triangle ADC \sim \triangle A'D'C'")
        popup_2.scale(0.9)
        popup_2.move_to((group_ADC[0].get_center() + group_ADC[1].get_center()) / 2 + DOWN * 4)

        # =============================
        # ANIMATION
        # =============================
        self.play(Create(triangle_ABC))
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(0.3)

        self.play(Create(triangle_big))
        self.play(Write(label_Ap), Write(label_Bp), Write(label_Cp))
        self.wait(0.3)

        # Vẽ phân giác và điểm D, D'
        self.play(FadeIn(D), FadeIn(D_p), Write(label_D), Write(label_Dp))
        self.play(Create(AD), Create(AD_p))
        self.wait(0.3)

        # Đánh dấu góc phân giác bằng nhau
        self.play(
            Create(angle_BAD),
            Create(angle_DAC),
            Create(angle_BpApDp),
            Create(angle_DpApCp),
            run_time=1
        )
        self.wait(0.5)

        # =============================
        # HIGHLIGHT CẶP ADB và A'D'B'
        # =============================
        self.play(
            tri_ADB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApDpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_1, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_1),
            tri_ADB.animate.set_fill(opacity=0),
            tri_ApDpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        # =============================
        # HIGHLIGHT CẶP ADC và A'D'C'
        # =============================
        self.play(
            tri_ADC.animate.set_fill(RED, opacity=0.45),
            tri_ApDpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_2, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_2),
            tri_ADC.animate.set_fill(opacity=0),
            tri_ApDpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

                # =============================
        # XÓA PHẦN PHÂN GIÁC
        # =============================
        self.play(
            FadeOut(AD), FadeOut(AD_p),
            FadeOut(D), FadeOut(D_p),
            FadeOut(label_D), FadeOut(label_Dp),
            FadeOut(angle_BAD), FadeOut(angle_DAC),
            FadeOut(angle_BpApDp), FadeOut(angle_DpApCp),
            run_time=0.8
        )

        # =============================
        # CHÂN ĐƯỜNG CAO H, H'
        # =============================
        def foot_of_perpendicular(P, X, Y):
            XY = Y - X
            t = np.dot(P - X, XY) / np.dot(XY, XY)
            return X + t * XY

        H_pos = foot_of_perpendicular(A, B, C)
        H_p_pos = foot_of_perpendicular(A_p, B_p, C_p)

        H = Dot(H_pos, color=WHITE)
        H_p = Dot(H_p_pos, color=WHITE)

        label_H = Text("H", font_size=28).next_to(H, DOWN)
        label_Hp = Text("H'", font_size=28).next_to(H_p, DOWN)

        # =============================
        # ĐƯỜNG CAO AH, A'H'
        # =============================
        AH = Line(A, H_pos, color=WHITE)
        AH_p = Line(A_p, H_p_pos, color=WHITE)

        # =============================
        # DẤU VUÔNG GÓC
        # =============================
        right_angle_H = RightAngle(
            Line(H_pos, A),
            Line(H_pos, B),
            length=0.18,
            color=GREEN
        )

        right_angle_Hp = RightAngle(
            Line(H_p_pos, A_p),
            Line(H_p_pos, B_p),
            length=0.22,
            color=GREEN
        )

        # =============================
        # CÁC TAM GIÁC CẦN HIGHLIGHT
        # =============================
        tri_AHB = Polygon(A, H_pos, B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ApHpBp = Polygon(A_p, H_p_pos, B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)

        tri_AHC = Polygon(A, H_pos, C, stroke_width=0, fill_color=RED, fill_opacity=0)
        tri_ApHpCp = Polygon(A_p, H_p_pos, C_p, stroke_width=0, fill_color=RED, fill_opacity=0)

        group_AHB = VGroup(tri_AHB, tri_ApHpBp)
        group_AHC = VGroup(tri_AHC, tri_ApHpCp)

        popup_3 = MathTex(r"\triangle AHB \sim \triangle A'H'B'")
        popup_3.scale(0.9)
        popup_3.move_to((group_AHB[0].get_center() + group_AHB[1].get_center()) / 2 + DOWN * 4)

        popup_4 = MathTex(r"\triangle AHC \sim \triangle A'H'C'")
        popup_4.scale(0.9)
        popup_4.move_to((group_AHC[0].get_center() + group_AHC[1].get_center()) / 2 + DOWN * 4)

        # =============================
        # VẼ ĐƯỜNG CAO
        # =============================
        self.play(FadeIn(H), FadeIn(H_p), Write(label_H), Write(label_Hp))
        self.play(Create(AH), Create(AH_p))
        self.wait(0.3)

        # Đánh dấu vuông góc
        self.play(Create(right_angle_H), Create(right_angle_Hp), run_time=0.8)
        self.wait(0.5)

        # =============================
        # HIGHLIGHT CẶP AHB và A'H'B'
        # =============================
        self.play(
            tri_AHB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApHpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_3, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_3),
            tri_AHB.animate.set_fill(opacity=0),
            tri_ApHpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        # =============================
        # HIGHLIGHT CẶP AHC và A'H'C'
        # =============================
        self.play(
            tri_AHC.animate.set_fill(RED, opacity=0.45),
            tri_ApHpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_4, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_4),
            tri_AHC.animate.set_fill(opacity=0),
            tri_ApHpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            FadeOut(AH), FadeOut(AH_p),
            FadeOut(H), FadeOut(H_p),
            FadeOut(label_H), FadeOut(label_Hp),
            FadeOut(right_angle_H), FadeOut(right_angle_Hp),
            run_time=0.8
        )

        # =============================
        # ĐIỂM E, E' CHUYỂN ĐỘNG TRÊN BC và B'C'
        # Dùng cùng tham số t để luôn đảm bảo:
        # EB/EC = E'B'/E'C'
        # =============================
        t_tracker = ValueTracker(0.3)

        def get_E():
            t = t_tracker.get_value()
            return B + t * (C - B)

        def get_Ep():
            t = t_tracker.get_value()
            return B_p + t * (C_p - B_p)

        E = always_redraw(lambda: Dot(get_E(), color=WHITE))
        E_p = always_redraw(lambda: Dot(get_Ep(), color=WHITE))

        label_E = always_redraw(lambda: Text("E", font_size=28).next_to(get_E(), DOWN))
        label_Ep = always_redraw(lambda: Text("E'", font_size=28).next_to(get_Ep(), DOWN))

        # =============================
        # ĐOẠN AE, A'E'
        # =============================
        AE = always_redraw(lambda: Line(A, get_E(), color=WHITE))
        AE_p = always_redraw(lambda: Line(A_p, get_Ep(), color=WHITE))

        # =============================
        # TỈ LỆ ĐỘNG
        # Nếu E = B + t(C-B) thì EB/EC = t/(1-t)
        # =============================
        def get_ratio():
            t = t_tracker.get_value()
            return t / (1 - t)

        ratio_text = always_redraw(
            lambda: VGroup(
                MathTex(
                    r"\frac{EB}{EC}=\frac{E'B'}{E'C'}=",
                    font_size=40
                ),
                DecimalNumber(
                    get_ratio(),
                    num_decimal_places=2,
                    font_size=40
                )
            ).arrange(RIGHT, buff=0.15).move_to(DOWN * 4)
        )

        # =============================
        # HIỆN E, E' VÀ CÁC ĐOẠN NỐI
        # =============================
        self.play(FadeIn(E), FadeIn(E_p), Write(label_E), Write(label_Ep))
        self.play(Create(AE), Create(AE_p))
        self.play(FadeIn(ratio_text))
        self.wait(0.3)

        # =============================
        # CHO E, E' CHUYỂN ĐỘNG
        # Vì dùng cùng t nên luôn bảo toàn tỉ lệ
        # =============================
        self.play(t_tracker.animate.set_value(0.68), run_time=2.2, rate_func=smooth)
        self.play(t_tracker.animate.set_value(0.42), run_time=1.8, rate_func=smooth)
        self.wait(0.3)

        # =============================
        # ẨN TỈ LỆ, GIỮ E VÀ E' ĐỨNG YÊN
        # =============================
        self.play(FadeOut(ratio_text), run_time=0.6)

        # =============================
        # CÁC TAM GIÁC CẦN HIGHLIGHT
        # Dùng always_redraw để bám theo E, E'
        # =============================
        tri_AEB = always_redraw(
            lambda: Polygon(A, get_E(), B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        )
        tri_ApEpBp = always_redraw(
            lambda: Polygon(A_p, get_Ep(), B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        )

        tri_AEC = always_redraw(
            lambda: Polygon(A, get_E(), C, stroke_width=0, fill_color=RED, fill_opacity=0)
        )
        tri_ApEpCp = always_redraw(
            lambda: Polygon(A_p, get_Ep(), C_p, stroke_width=0, fill_color=RED, fill_opacity=0)
        )

        popup_5 = MathTex(r"\triangle AEB \sim \triangle A'E'B'")
        popup_5.scale(0.9)
        popup_5.move_to(DOWN * 4.8)

        popup_6 = MathTex(r"\triangle AEC \sim \triangle A'E'C'")
        popup_6.scale(0.9)
        popup_6.move_to(DOWN * 4.8)

        # add trước để animate fill ổn định
        self.add(tri_AEB, tri_ApEpBp, tri_AEC, tri_ApEpCp)

        # =============================
        # HIGHLIGHT CẶP AEB và A'E'B'
        # =============================
        self.play(
            tri_AEB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApEpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_5, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_5),
            tri_AEB.animate.set_fill(opacity=0),
            tri_ApEpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        # =============================
        # HIGHLIGHT CẶP AEC và A'E'C'
        # =============================
        self.play(
            tri_AEC.animate.set_fill(RED, opacity=0.45),
            tri_ApEpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_6, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_6),
            tri_AEC.animate.set_fill(opacity=0),
            tri_ApEpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

                # =============================
        # ẨN PHẦN E, E'
        # =============================
        self.play(
            FadeOut(AE), FadeOut(AE_p),
            FadeOut(E), FadeOut(E_p),
            FadeOut(label_E), FadeOut(label_Ep),
            run_time=0.8
        )

        # Nếu còn các tam giác highlight của phần E thì xóa luôn
        self.remove(tri_AEB, tri_ApEpBp, tri_AEC, tri_ApEpCp)

        # =============================
        # F, F' CHUYỂN ĐỘNG TRÊN BC, B'C'
        # sao cho góc BAF = B'A'F'
        # =============================
        s_tracker = ValueTracker(0.25)

        def get_F():
            s = s_tracker.get_value()
            return B + s * (C - B)

        def get_Fp():
            s = s_tracker.get_value()
            return B_p + s * (C_p - B_p)

        F = always_redraw(lambda: Dot(get_F(), color=WHITE))
        F_p = always_redraw(lambda: Dot(get_Fp(), color=WHITE))

        label_F = always_redraw(lambda: Text("F", font_size=28).next_to(get_F(), DOWN))
        label_Fp = always_redraw(lambda: Text("F'", font_size=28).next_to(get_Fp(), DOWN))

        AF = always_redraw(lambda: Line(A, get_F(), color=WHITE))
        AF_p = always_redraw(lambda: Line(A_p, get_Fp(), color=WHITE))

        # =============================
        # HÀM TẠO CUNG ĐÁNH DẤU GÓC
        # =============================
        def make_dynamic_angle_mark(vertex_func, p1_func, p2_func, radius=0.32, color=GREEN):
            def build_arc():
                vertex = vertex_func()
                p1 = p1_func()
                p2 = p2_func()

                u1 = p1 - vertex
                u2 = p2 - vertex

                a1 = np.arctan2(u1[1], u1[0])
                a2 = np.arctan2(u2[1], u2[0])

                diff = (a2 - a1) % (2 * np.pi)
                if diff > np.pi:
                    a1, a2 = a2, a1
                    diff = (a2 - a1) % (2 * np.pi)

                return Arc(
                    radius=radius,
                    start_angle=a1,
                    angle=diff,
                    arc_center=vertex,
                    color=color,
                    stroke_width=3
                )
            return always_redraw(build_arc)

        # Góc BAF và B'A'F'
        angle_BAF = make_dynamic_angle_mark(lambda: A, lambda: B, lambda: get_F(), radius=0.32, color=GREEN)
        angle_BpApFp = make_dynamic_angle_mark(lambda: A_p, lambda: B_p, lambda: get_Fp(), radius=0.38, color=GREEN)

        # =============================
        # SỐ ĐO GÓC ĐỘNG
        # =============================
        def angle_deg(P, Q, R):
            # góc PQR
            v1 = P - Q
            v2 = R - Q
            cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cos_theta = np.clip(cos_theta, -1, 1)
            return np.degrees(np.arccos(cos_theta))

        angle_text = always_redraw(
            lambda: VGroup(
                MathTex(r"\angle BAF=\angle B'A'F'=", font_size=38),
                DecimalNumber(
                    angle_deg(B, A, get_F()),
                    num_decimal_places=1,
                    font_size=38
                ),
                MathTex(r"^\circ", font_size=38)
            ).arrange(RIGHT, buff=0.12).move_to(DOWN * 6.0)
        )

        # =============================
        # HIỆN F, F' VÀ CÁC ĐỐI TƯỢNG LIÊN QUAN
        # =============================
        self.play(FadeIn(F), FadeIn(F_p), Write(label_F), Write(label_Fp))
        self.play(Create(AF), Create(AF_p))
        self.play(Create(angle_BAF), Create(angle_BpApFp))
        self.play(FadeIn(angle_text))
        self.wait(0.3)

        # =============================
        # CHUYỂN ĐỘNG GIỮ ĐIỀU KIỆN GÓC BẰNG NHAU
        # =============================
        self.play(s_tracker.animate.set_value(0.72), run_time=2.2, rate_func=smooth)
        self.play(s_tracker.animate.set_value(0.43), run_time=1.8, rate_func=smooth)
        self.wait(0.3)

        # =============================
        # ẨN SỐ ĐO GÓC, GIỮ F VÀ F' ĐỨNG YÊN
        # =============================
        self.play(FadeOut(angle_text), run_time=0.6)

        # =============================
        # HIGHLIGHT CÁC CẶP TAM GIÁC
        # =============================
        tri_AFB = always_redraw(
            lambda: Polygon(A, get_F(), B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        )
        tri_ApFpBp = always_redraw(
            lambda: Polygon(A_p, get_Fp(), B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        )

        tri_AFC = always_redraw(
            lambda: Polygon(A, get_F(), C, stroke_width=0, fill_color=RED, fill_opacity=0)
        )
        tri_ApFpCp = always_redraw(
            lambda: Polygon(A_p, get_Fp(), C_p, stroke_width=0, fill_color=RED, fill_opacity=0)
        )

        popup_7 = MathTex(r"\triangle AFB \sim \triangle A'F'B'")
        popup_7.scale(0.9)
        popup_7.move_to(DOWN * 4.8)

        popup_8 = MathTex(r"\triangle AFC \sim \triangle A'F'C'")
        popup_8.scale(0.9)
        popup_8.move_to(DOWN * 4.8)

        self.add(tri_AFB, tri_ApFpBp, tri_AFC, tri_ApFpCp)

        # =============================
        # HIGHLIGHT CẶP AFB và A'F'B'
        # =============================
        self.play(
            tri_AFB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApFpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_7, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_7),
            tri_AFB.animate.set_fill(opacity=0),
            tri_ApFpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        # =============================
        # HIGHLIGHT CẶP AFC và A'F'C'
        # =============================
        self.play(
            tri_AFC.animate.set_fill(RED, opacity=0.45),
            tri_ApFpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_8, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_8),
            tri_AFC.animate.set_fill(opacity=0),
            tri_ApFpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        # =============================
        # CHUYỂN CẢNH KIỂU LẬT/TRANG QUÉT NGANG
        # =============================
        page_cover = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )

        # đặt tấm che ở ngoài mép phải trước
        page_cover.move_to(RIGHT * config.frame_width)

        self.play(
            page_cover.animate.move_to(ORIGIN),
            run_time=1.0,
            rate_func=smooth
        )

        self.wait(0.3)