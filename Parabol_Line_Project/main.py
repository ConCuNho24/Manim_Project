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
        A = LEFT * 2.5 + UP * 0.5
        B = LEFT * 4.0 + DOWN * 1.5
        C = LEFT * 1.9 + DOWN * 1.5

        triangle_ABC = Polygon(A, B, C, color=BLUE)

        label_A = Text("A", font_size = 16).next_to(A, UP)
        label_B = Text("B", font_size = 16).next_to(B, DOWN)
        label_C = Text("C", font_size = 16).next_to(C, DOWN)

        # =============================
        # TAM GIÁC A'B'C' (BÊN PHẢI - ĐỒNG DẠNG, LỚN HƠN)
        # =============================
        scale_factor = 1.5

        A_p = RIGHT * 1.6 + UP * 1.5
        B_p = A_p + (B - A) * scale_factor
        C_p = A_p + (C - A) * scale_factor

        triangle_big = Polygon(A_p, B_p, C_p, color=YELLOW)

        label_Ap = Text("A'", font_size = 16).next_to(A_p, UP)
        label_Bp = Text("B'", font_size = 16).next_to(B_p, DOWN)
        label_Cp = Text("C'", font_size = 16).next_to(C_p, DOWN)

        # =============================
        # HÀM PHỤ
        # =============================
        def make_tick_on_segment(P, Q, center, length=0.18, color=WHITE, stroke_width=3):
            direction = Q - P
            unit_dir = direction / np.linalg.norm(direction)
            perp = np.array([-unit_dir[1], unit_dir[0], 0])
            tick = Line(
                center - perp * length / 2,
                center + perp * length / 2,
                color=color,
                stroke_width=stroke_width
            )
            return tick

        def angle_bisector_foot(PA, PB, PC):
            AB_len = np.linalg.norm(PB - PA)
            AC_len = np.linalg.norm(PC - PA)
            t = AB_len / (AB_len + AC_len)
            return PB + t * (PC - PB)

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

        def foot_of_perpendicular(P, X, Y):
            XY = Y - X
            t = np.dot(P - X, XY) / np.dot(XY, XY)
            return X + t * XY

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

        def angle_deg(P, Q, R):
            v1 = P - Q
            v2 = R - Q
            cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            cos_theta = np.clip(cos_theta, -1, 1)
            return np.degrees(np.arccos(cos_theta))

        def rigid_transform_triangle(PA, PB, PC, QA, QB):
            """
            Chỉ quay + tịnh tiến, không scale.
            PA -> QA và đoạn PA PB quay thành cùng phương QA QB.
            """
            v1 = PB - PA
            v2 = QB - QA

            ang1 = np.arctan2(v1[1], v1[0])
            ang2 = np.arctan2(v2[1], v2[0])
            theta = ang2 - ang1

            rot = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta),  np.cos(theta), 0],
                [0, 0, 1]
            ])

            def map_point(X):
                Y = X - PA
                Y = rot @ Y
                return QA + Y

            return map_point(PA), map_point(PB), map_point(PC)

        # =============================
        # VẼ 2 TAM GIÁC GỐC
        # =============================
        self.play(Create(triangle_ABC))
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(0.3)

        self.play(Create(triangle_big))
        self.play(Write(label_Ap), Write(label_Bp), Write(label_Cp))
        self.wait(0.3)

        # =========================================================
        # 1) TRUNG TUYẾN
        # =========================================================
        M_pos = (B + C) / 2
        M = Dot(M_pos, color=WHITE)
        label_M = Text("M", font_size = 16).next_to(M, DOWN)

        M_p_pos = (B_p + C_p) / 2
        M_p = Dot(M_p_pos, color=WHITE)
        label_Mp = Text("M'", font_size = 16).next_to(M_p, DOWN)

        AM = Line(A, M_pos, color=WHITE)
        APM = Line(A_p, M_p_pos, color=WHITE)

        mid_MB = (M_pos + B) / 2
        mid_MC = (M_pos + C) / 2

        tick_MB = make_tick_on_segment(M_pos, B, mid_MB, length=0.18)
        tick_MC = make_tick_on_segment(M_pos, C, mid_MC, length=0.18)

        mid_MpBp = (M_p_pos + B_p) / 2
        mid_MpCp = (M_p_pos + C_p) / 2
        offset = 0.08

        dir_MpBp = B_p - M_p_pos
        unit_MpBp = dir_MpBp / np.linalg.norm(dir_MpBp)

        dir_MpCp = C_p - M_p_pos
        unit_MpCp = dir_MpCp / np.linalg.norm(dir_MpCp)

        tick1_MpBp = make_tick_on_segment(M_p_pos, B_p, mid_MpBp - unit_MpBp * offset, length=0.2)
        tick2_MpBp = make_tick_on_segment(M_p_pos, B_p, mid_MpBp + unit_MpBp * offset, length=0.2)

        tick1_MpCp = make_tick_on_segment(M_p_pos, C_p, mid_MpCp - unit_MpCp * offset, length=0.2)
        tick2_MpCp = make_tick_on_segment(M_p_pos, C_p, mid_MpCp + unit_MpCp * offset, length=0.2)

        tri_AMB = Polygon(A, M_pos, B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ApMpBp = Polygon(A_p, M_p_pos, B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_AMC = Polygon(A, M_pos, C, stroke_width=0, fill_color=RED, fill_opacity=0)
        tri_ApMpCp = Polygon(A_p, M_p_pos, C_p, stroke_width=0, fill_color=RED, fill_opacity=0)

        group_AMB = VGroup(tri_AMB, tri_ApMpBp)
        group_AMC = VGroup(tri_AMC, tri_ApMpCp)

        popup_1 = MathTex(r"\triangle AMB \sim \triangle A'M'B'")
        popup_1.scale(0.9)
        popup_1.move_to((group_AMB[0].get_center() + group_AMB[1].get_center()) / 2 + DOWN * 4)

        popup_2 = MathTex(r"\triangle AMC \sim \triangle A'M'C'")
        popup_2.scale(0.9)
        popup_2.move_to((group_AMC[0].get_center() + group_AMC[1].get_center()) / 2 + DOWN * 4)

        self.play(FadeIn(M), FadeIn(M_p), Write(label_M), Write(label_Mp))
        self.play(Create(AM), Create(APM))
        self.play(Create(tick_MB), Create(tick_MC))
        self.play(
            Create(tick1_MpBp), Create(tick2_MpBp),
            Create(tick1_MpCp), Create(tick2_MpCp)
        )
        self.wait(0.5)

        self.play(
            tri_AMB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApMpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_1, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_1),
            tri_AMB.animate.set_fill(opacity=0),
            tri_ApMpBp.animate.set_fill(opacity=0),
        )

        self.play(
            tri_AMC.animate.set_fill(RED, opacity=0.45),
            tri_ApMpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_2, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_2),
            tri_AMC.animate.set_fill(opacity=0),
            tri_ApMpCp.animate.set_fill(opacity=0),
        )

        self.play(
            FadeOut(AM), FadeOut(APM),
            FadeOut(M), FadeOut(M_p),
            FadeOut(label_M), FadeOut(label_Mp),
            FadeOut(tick_MB), FadeOut(tick_MC),
            FadeOut(tick1_MpBp), FadeOut(tick2_MpBp),
            FadeOut(tick1_MpCp), FadeOut(tick2_MpCp),
            run_time=1
        )

        self.wait(0.5)

        # =========================================================
        # 2) PHÂN GIÁC
        # =========================================================
        D_pos = angle_bisector_foot(A, B, C)
        D_p_pos = angle_bisector_foot(A_p, B_p, C_p)

        D = Dot(D_pos, color=WHITE)
        D_p = Dot(D_p_pos, color=WHITE)

        label_D = Text("D", font_size = 16).next_to(D, DOWN)
        label_Dp = Text("D'", font_size = 16).next_to(D_p, DOWN)

        AD = Line(A, D_pos, color=WHITE)
        AD_p = Line(A_p, D_p_pos, color=WHITE)

        angle_BAD = make_angle_marks(A, B, D_pos, radius=0.30, color=GREEN)
        angle_DAC = make_angle_marks(A, D_pos, C, radius=0.40, color=GREEN)

        angle_BpApDp = make_angle_marks(A_p, B_p, D_p_pos, radius=0.34, color=GREEN)
        angle_DpApCp = make_angle_marks(A_p, D_p_pos, C_p, radius=0.45, color=GREEN)

        tri_ADB = Polygon(A, D_pos, B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ApDpBp = Polygon(A_p, D_p_pos, B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ADC = Polygon(A, D_pos, C, stroke_width=0, fill_color=RED, fill_opacity=0)
        tri_ApDpCp = Polygon(A_p, D_p_pos, C_p, stroke_width=0, fill_color=RED, fill_opacity=0)

        group_ADB = VGroup(tri_ADB, tri_ApDpBp)
        group_ADC = VGroup(tri_ADC, tri_ApDpCp)

        popup_3 = MathTex(r"\triangle ADB \sim \triangle A'D'B'")
        popup_3.scale(0.9)
        popup_3.move_to((group_ADB[0].get_center() + group_ADB[1].get_center()) / 2 + DOWN * 4)

        popup_4 = MathTex(r"\triangle ADC \sim \triangle A'D'C'")
        popup_4.scale(0.9)
        popup_4.move_to((group_ADC[0].get_center() + group_ADC[1].get_center()) / 2 + DOWN * 4)

        self.play(FadeIn(D), FadeIn(D_p), Write(label_D), Write(label_Dp))
        self.play(Create(AD), Create(AD_p))
        self.wait(0.3)

        self.play(
            Create(angle_BAD),
            Create(angle_DAC),
            Create(angle_BpApDp),
            Create(angle_DpApCp),
            run_time=1
        )
        self.wait(0.5)

        self.play(
            tri_ADB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApDpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_3, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_3),
            tri_ADB.animate.set_fill(opacity=0),
            tri_ApDpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            tri_ADC.animate.set_fill(RED, opacity=0.45),
            tri_ApDpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_4, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_4),
            tri_ADC.animate.set_fill(opacity=0),
            tri_ApDpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            FadeOut(AD), FadeOut(AD_p),
            FadeOut(D), FadeOut(D_p),
            FadeOut(label_D), FadeOut(label_Dp),
            FadeOut(angle_BAD), FadeOut(angle_DAC),
            FadeOut(angle_BpApDp), FadeOut(angle_DpApCp),
            run_time=0.8
        )

        # =========================================================
        # 3) ĐƯỜNG CAO
        # =========================================================
        H_pos = foot_of_perpendicular(A, B, C)
        H_p_pos = foot_of_perpendicular(A_p, B_p, C_p)

        H = Dot(H_pos, color=WHITE)
        H_p = Dot(H_p_pos, color=WHITE)

        label_H = Text("H", font_size = 16).next_to(H, DOWN)
        label_Hp = Text("H'", font_size = 16).next_to(H_p, DOWN)

        AH = Line(A, H_pos, color=WHITE)
        AH_p = Line(A_p, H_p_pos, color=WHITE)

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

        tri_AHB = Polygon(A, H_pos, B, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_ApHpBp = Polygon(A_p, H_p_pos, B_p, stroke_width=0, fill_color=GREEN, fill_opacity=0)
        tri_AHC = Polygon(A, H_pos, C, stroke_width=0, fill_color=RED, fill_opacity=0)
        tri_ApHpCp = Polygon(A_p, H_p_pos, C_p, stroke_width=0, fill_color=RED, fill_opacity=0)

        group_AHB = VGroup(tri_AHB, tri_ApHpBp)
        group_AHC = VGroup(tri_AHC, tri_ApHpCp)

        popup_5 = MathTex(r"\triangle AHB \sim \triangle A'H'B'")
        popup_5.scale(0.9)
        popup_5.move_to((group_AHB[0].get_center() + group_AHB[1].get_center()) / 2 + DOWN * 4)

        popup_6 = MathTex(r"\triangle AHC \sim \triangle A'H'C'")
        popup_6.scale(0.9)
        popup_6.move_to((group_AHC[0].get_center() + group_AHC[1].get_center()) / 2 + DOWN * 4)

        self.play(FadeIn(H), FadeIn(H_p), Write(label_H), Write(label_Hp))
        self.play(Create(AH), Create(AH_p))
        self.wait(0.3)

        self.play(Create(right_angle_H), Create(right_angle_Hp), run_time=0.8)
        self.wait(0.5)

        self.play(
            tri_AHB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApHpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_5, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_5),
            tri_AHB.animate.set_fill(opacity=0),
            tri_ApHpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            tri_AHC.animate.set_fill(RED, opacity=0.45),
            tri_ApHpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_6, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_6),
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

        # =========================================================
        # 4) ĐIỂM E, E' CHUYỂN ĐỘNG THEO TỈ LỆ
        # =========================================================
        t_tracker = ValueTracker(0.3)

        def get_E():
            t = t_tracker.get_value()
            return B + t * (C - B)

        def get_Ep():
            t = t_tracker.get_value()
            return B_p + t * (C_p - B_p)

        E = always_redraw(lambda: Dot(get_E(), color=WHITE))
        E_p = always_redraw(lambda: Dot(get_Ep(), color=WHITE))

        label_E = always_redraw(lambda: Text("E", font_size = 16).next_to(get_E(), DOWN))
        label_Ep = always_redraw(lambda: Text("E'", font_size = 16).next_to(get_Ep(), DOWN))

        AE = always_redraw(lambda: Line(A, get_E(), color=WHITE))
        AE_p = always_redraw(lambda: Line(A_p, get_Ep(), color=WHITE))

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

        self.play(FadeIn(E), FadeIn(E_p), Write(label_E), Write(label_Ep))
        self.play(Create(AE), Create(AE_p))
        self.play(FadeIn(ratio_text))
        self.wait(0.3)

        self.play(t_tracker.animate.set_value(0.68), run_time=2.2, rate_func=smooth)
        self.play(t_tracker.animate.set_value(0.42), run_time=1.8, rate_func=smooth)
        self.wait(0.3)

        self.play(FadeOut(ratio_text), run_time=0.6)

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

        popup_7 = MathTex(r"\triangle AEB \sim \triangle A'E'B'")
        popup_7.scale(0.9)
        popup_7.move_to(DOWN * 4.8)

        popup_8 = MathTex(r"\triangle AEC \sim \triangle A'E'C'")
        popup_8.scale(0.9)
        popup_8.move_to(DOWN * 4.8)

        self.add(tri_AEB, tri_ApEpBp, tri_AEC, tri_ApEpCp)

        self.play(
            tri_AEB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApEpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_7, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_7),
            tri_AEB.animate.set_fill(opacity=0),
            tri_ApEpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            tri_AEC.animate.set_fill(RED, opacity=0.45),
            tri_ApEpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_8, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_8),
            tri_AEC.animate.set_fill(opacity=0),
            tri_ApEpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            FadeOut(AE), FadeOut(AE_p),
            FadeOut(E), FadeOut(E_p),
            FadeOut(label_E), FadeOut(label_Ep),
            run_time=0.8
        )

        self.remove(tri_AEB, tri_ApEpBp, tri_AEC, tri_ApEpCp)

        # =========================================================
        # 5) ĐIỂM F, F' CHUYỂN ĐỘNG THEO GÓC
        # =========================================================
        s_tracker = ValueTracker(0.25)

        def get_F():
            s = s_tracker.get_value()
            return B + s * (C - B)

        def get_Fp():
            s = s_tracker.get_value()
            return B_p + s * (C_p - B_p)

        F = always_redraw(lambda: Dot(get_F(), color=WHITE))
        F_p = always_redraw(lambda: Dot(get_Fp(), color=WHITE))

        label_F = always_redraw(lambda: Text("F", font_size = 16).next_to(get_F(), DOWN))
        label_Fp = always_redraw(lambda: Text("F'", font_size = 16).next_to(get_Fp(), DOWN))

        AF = always_redraw(lambda: Line(A, get_F(), color=WHITE))
        AF_p = always_redraw(lambda: Line(A_p, get_Fp(), color=WHITE))

        angle_BAF = make_dynamic_angle_mark(lambda: A, lambda: B, lambda: get_F(), radius=0.32, color=GREEN)
        angle_BpApFp = make_dynamic_angle_mark(lambda: A_p, lambda: B_p, lambda: get_Fp(), radius=0.38, color=GREEN)

        angle_text = always_redraw(
            lambda: VGroup(
                MathTex(r"\angle BAF=\angle B'A'F'=", font_size=38),
                DecimalNumber(
                    angle_deg(B, A, get_F()),
                    num_decimal_places=1,
                    font_size=38
                ),
                MathTex(r"^\circ", font_size=38)
            ).arrange(RIGHT, buff=0.12).move_to(DOWN * 4)
        )

        self.play(FadeIn(F), FadeIn(F_p), Write(label_F), Write(label_Fp))
        self.play(Create(AF), Create(AF_p))
        self.play(Create(angle_BAF), Create(angle_BpApFp))
        self.play(FadeIn(angle_text))
        self.wait(0.3)

        self.play(s_tracker.animate.set_value(0.72), run_time=2.2, rate_func=smooth)
        self.play(s_tracker.animate.set_value(0.43), run_time=1.8, rate_func=smooth)
        self.wait(0.3)

        self.play(FadeOut(angle_text), run_time=0.6)

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

        popup_9 = MathTex(r"\triangle AFB \sim \triangle A'F'B'")
        popup_9.scale(0.9)
        popup_9.move_to(DOWN * 4.8)

        popup_10 = MathTex(r"\triangle AFC \sim \triangle A'F'C'")
        popup_10.scale(0.9)
        popup_10.move_to(DOWN * 4.8)

        self.add(tri_AFB, tri_ApFpBp, tri_AFC, tri_ApFpCp)

        self.play(
            tri_AFB.animate.set_fill(GREEN, opacity=0.45),
            tri_ApFpBp.animate.set_fill(GREEN, opacity=0.45),
            FadeIn(popup_9, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1)

        self.play(
            FadeOut(popup_9),
            tri_AFB.animate.set_fill(opacity=0),
            tri_ApFpBp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            tri_AFC.animate.set_fill(RED, opacity=0.45),
            tri_ApFpCp.animate.set_fill(RED, opacity=0.45),
            FadeIn(popup_10, shift=DOWN * 0.3),
            run_time=1
        )
        self.wait(1.5)

        self.play(
            FadeOut(popup_10),
            tri_AFC.animate.set_fill(opacity=0),
            tri_ApFpCp.animate.set_fill(opacity=0),
            run_time=0.8
        )

        self.play(
            FadeOut(AF), FadeOut(AF_p),
            FadeOut(F), FadeOut(F_p),
            FadeOut(label_F), FadeOut(label_Fp),
            FadeOut(angle_BAF), FadeOut(angle_BpApFp),
            run_time=0.8
        )

        self.remove(tri_AFB, tri_ApFpBp, tri_AFC, tri_ApFpCp)

        self.wait(0.3)

        # =========================================================
        # 6) TAM GIÁC MNP, M'N'P' Ở DƯỚI
        #    BÊN PHẢI: A'B'C' DỊCH LÊN, M'N'P' ĐI THEO VÀ GHÉP VÀO
        # =========================================================
        BC_len = np.linalg.norm(C - B)
        MN_len = BC_len * 1.35

        M0 = np.array([B[0], -4.8, 0])
        N0 = M0 + np.array([MN_len, 0, 0])
        P0 = (M0 + N0) / 2 + np.array([0, -1.6, 0])

        triangle_MNP = Polygon(M0, N0, P0, color=TEAL)
        label_M0 = Text("M", font_size=16).next_to(M0, LEFT)
        label_N0 = Text("N", font_size=16).next_to(N0, UP)
        label_P0 = Text("P", font_size=16).next_to(P0, DOWN)

        BpCp_len = np.linalg.norm(C_p - B_p)
        MpNp_len = BpCp_len * 1.35

        M0_p = np.array([B_p[0], -4.8, 0])
        N0_p = M0_p + np.array([MpNp_len, 0, 0])
        P0_p = (M0_p + N0_p) / 2 + np.array([0, -2.0, 0])

        triangle_MpNpPp = Polygon(M0_p, N0_p, P0_p, color=ORANGE)
        label_M0p = Text("M'", font_size=16).next_to(M0_p, UP)
        label_N0p = Text("N'", font_size=16).next_to(N0_p, RIGHT)
        label_P0p = Text("P'", font_size=16).next_to(P0_p, DOWN)

        self.play(
            Create(triangle_MNP),
            Write(label_M0), Write(label_N0), Write(label_P0),
            Create(triangle_MpNpPp),
            Write(label_M0p), Write(label_N0p), Write(label_P0p),
            run_time=1.2
        )
        self.wait(0.5)

        # =============================
        # BÊN TRÁI: ghép bằng phép cứng
        # =============================
        M1, N1, P1 = rigid_transform_triangle(M0, N0, P0, B, C)

        triangle_MNP_fit = Polygon(M1, N1, P1, color=TEAL)
        label_M_fit = Text("M", font_size=16).next_to(M1, LEFT)
        label_N_fit = Text("N", font_size=16).next_to(N1, RIGHT)
        label_P_fit = Text("P", font_size=16).next_to(P1, DOWN)

        # =============================
        # BÊN PHẢI: trước hết dịch A'B'C' lên trên
        # rồi mới ghép M'N'P' theo B'C' mới
        # =============================
        shift_up = UP * 1.6

        A_p_new = A_p + shift_up
        B_p_new = B_p + shift_up
        C_p_new = C_p + shift_up

        triangle_big_shifted = Polygon(A_p_new, B_p_new, C_p_new, color=YELLOW)
        label_Ap_shifted = Text("A'", font_size=16).next_to(A_p_new, UP)
        label_Bp_shifted = Text("B'", font_size=16).next_to(B_p_new, DOWN)
        label_Cp_shifted = Text("C'", font_size=16).next_to(C_p_new, DOWN)

        Mp1, Np1, Pp1 = rigid_transform_triangle(M0_p, N0_p, P0_p, B_p_new, C_p_new)

        triangle_MpNpPp_fit = Polygon(Mp1, Np1, Pp1, color=ORANGE)
        label_Mp_fit = Text("M'", font_size=16).next_to(Mp1, LEFT)
        label_Np_fit = Text("N'", font_size=16).next_to(Np1, RIGHT)
        label_Pp_fit = Text("P'", font_size=16).next_to(Pp1, DOWN)

        # =============================
        # ANIMATE GHÉP
        # =============================
        self.play(
            Transform(triangle_MNP, triangle_MNP_fit),
            Transform(label_M0, label_M_fit),
            Transform(label_N0, label_N_fit),
            Transform(label_P0, label_P_fit),

            Transform(triangle_big, triangle_big_shifted),
            Transform(label_Ap, label_Ap_shifted),
            Transform(label_Bp, label_Bp_shifted),
            Transform(label_Cp, label_Cp_shifted),

            Transform(triangle_MpNpPp, triangle_MpNpPp_fit),
            Transform(label_M0p, label_Mp_fit),
            Transform(label_N0p, label_Np_fit),
            Transform(label_P0p, label_Pp_fit),
            run_time=2
        )

        self.wait(0.3)

        # =============================
        # ẨN LABEL M và M'
        # =============================
        self.play(
            FadeOut(label_M0),
            FadeOut(label_M0p),
            run_time=0.5
        )

        # =============================
        # HIGHLIGHT CÙNG MÀU
        # - cặp tam giác lớn: ABC và A'B'C'
        # - cặp tam giác phụ: MNP và M'N'P'
        # =============================
        tri_big_left_fill = Polygon(A, B, C, stroke_width=0, fill_color=BLUE, fill_opacity=0)
        tri_big_right_fill = Polygon(A_p_new, B_p_new, C_p_new, stroke_width=0, fill_color=BLUE, fill_opacity=0)

        tri_small_left_fill = Polygon(M1, N1, P1, stroke_width=0, fill_color=PURPLE, fill_opacity=0)
        tri_small_right_fill = Polygon(Mp1, Np1, Pp1, stroke_width=0, fill_color=PURPLE, fill_opacity=0)

        popup_big = MathTex(r"\triangle ABC \sim \triangle A'B'C'")
        popup_big.scale(0.9)
        popup_big.move_to(DOWN * 4.8)

        popup_small = MathTex(r"\triangle MNP \sim \triangle M'N'P'")
        popup_small.scale(0.9)
        popup_small.move_to(DOWN * 5.6)

        self.add(tri_big_left_fill, tri_big_right_fill, tri_small_left_fill, tri_small_right_fill)

        self.play(
            tri_big_left_fill.animate.set_fill(BLUE, opacity=0.35),
            tri_big_right_fill.animate.set_fill(BLUE, opacity=0.35),
            tri_small_left_fill.animate.set_fill(PURPLE, opacity=0.35),
            tri_small_right_fill.animate.set_fill(PURPLE, opacity=0.35),
            FadeIn(popup_big, shift=DOWN * 0.2),
            FadeIn(popup_small, shift=DOWN * 0.2),
            run_time=1.2
        )

        # =============================
        # HIGHLIGHT CÁC ĐOẠN BẰNG ĐƯỜNG VIỀN ĐỎ
        # =============================

        # --- BÊN TRÁI ---
        line_AB = Line(A, B, color=RED, stroke_width=6)
        line_MP = Line(M1, P1, color=RED, stroke_width=6)
        line_PN = Line(P1, N1, color=RED, stroke_width=6)
        line_NC = Line(N1, C, color=RED, stroke_width=6)
        line_AC = Line(A, C, color=RED, stroke_width=6)

        # --- BÊN PHẢI ---
        line_ApBp = Line(A_p_new, B_p_new, color=RED, stroke_width=6)
        line_MpPp = Line(Mp1, Pp1, color=RED, stroke_width=6)
        line_PpNp = Line(Pp1, Np1, color=RED, stroke_width=6)
        line_NpCp = Line(Np1, C_p_new, color=RED, stroke_width=6)
        line_ApCp = Line(A_p_new, C_p_new, color=RED, stroke_width=6)

        self.play(
            Create(line_AB),
            Create(line_MP),
            Create(line_PN),
            Create(line_NC),
            Create(line_AC),

            Create(line_ApBp),
            Create(line_MpPp),
            Create(line_PpNp),
            Create(line_NpCp),
            Create(line_ApCp),
            run_time=1.5
        )

        self.wait(0.5)

        # =============================
        # NỐI AN và A'N'
        # =============================
        line_AN = Line(A, N1, color=GREEN, stroke_width=6)
        line_ApNp = Line(A_p_new, Np1, color=GREEN, stroke_width=6)

        self.play(
            Create(line_AN),
            Create(line_ApNp),
            run_time=1
        )

        # =============================
        # ẨN TEXT CŨ
        # =============================
        self.play(
            FadeOut(popup_big),
            FadeOut(popup_small),
            run_time=0.5
        )

        # =============================
        # HIGHLIGHT ACN và A'C'N'
        # =============================
        tri_ACN_fill = Polygon(
            A, C, N1,
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0
        )
        tri_ApCpNp_fill = Polygon(
            A_p_new, C_p_new, Np1,
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=0
        )

        popup_new = MathTex(r"\triangle ACN \sim \triangle A'C'N'")
        popup_new.scale(0.95)
        popup_new.move_to(DOWN * 5.2)

        self.add(tri_ACN_fill, tri_ApCpNp_fill)

        self.play(
            tri_ACN_fill.animate.set_fill(GREEN, opacity=0.4),
            tri_ApCpNp_fill.animate.set_fill(GREEN, opacity=0.4),
            FadeIn(popup_new, shift=DOWN * 0.2),
            run_time=1.2
        )

        self.wait(2)