def get_coordinates(video_path):
# 🟥 Координаты рамки и синих линий под разные видео
    if "50kmh_mugur_jaunolaine" in video_path.lower():
        # Красная рамка
        x1, y1 = 5000, 2900      # Augšējais labais stūris
        x2, y2 = 4000, 2900     # Augšējais kreisais stūris
        x3, y3 = 7400, 6000     # Kreisais apakšējais stūris
        x4, y4 = 10500, 4600    # Apakšējais labais stūris
        distance_m = 200

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_prieksa_jaunolaine" in video_path.lower():
        # Красная рамка
        x1, y1 = 5200, 3000     # Augšējais labais stūris
        x2, y2 = 4900, 3000     # Augšējais kreisais stūris
        x3, y3 = 7950, 5500     # Kreisais apakšējais stūris
        x4, y4 = 11000, 4800    # Apakšējais labais stūris
        distance_m = 60

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 4950, 3100           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5550, 3075           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5500     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 11000, 4750    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_mugur_jaunolaine" in video_path.lower():
        # Красная рамка
        x1, y1 = 4950, 2850     # Augšējais labais stūris
        x2, y2 = 3950, 2850     # Augšējais kreisais stūris
        x3, y3 = 7300, 5900     # Kreisais apakšējais stūris
        x4, y4 = 10400, 4550     # Apakšējais labais stūris
        distance_m = 200

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_prieksa_jaunolaine" in video_path.lower():
        # Красная рамка
        x1, y1 = 5150, 3000   # Augšējais labais stūris
        x2, y2 = 4750, 3000   # Augšējais kreisais stūris
        x3, y3 = 8000, 6000   # Kreisais apakšējais stūris
        x4, y4 = 10700, 4600  # Apakšējais labais stūris
        distance_m = 60

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 5200, 3025         # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 4800, 3050         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7950, 5950   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10650, 4550  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_ropazi" in video_path.lower():
        # Красная рамка
        x1, y1 = 6400, 2900     # Augšējais labais stūris
        x2, y2 = 5700, 2900     # Augšējais kreisais stūris
        x3, y3 = 500, 5800      # Kreisais apakšējais stūris
        x4, y4 = 6900, 5800     # Apakšējais labais stūris
        distance_m = 150

        # 🟦 Синие линии (наклонные)
        blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_ropazi" in video_path.lower():
        # Красная рамка
        x1, y1 = 6400, 3200     # Augšējais labais stūris
        x2, y2 = 5700, 3200     # Augšējais Kreisais stūris
        x3, y3 = 500, 5700     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6200    # labais apakšējais stūris
        distance_m =45

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 5350, 3275           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6400, 3275           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1050, 5500     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6450, 5900    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "80kmh_ropazi" in video_path.lower():
        # Красная рамка
        x1, y1 = 6600, 3000     # Augšējais labais stūris
        x2, y2 = 5900, 3000     # Augšējais kreisais stūris
        x3, y3 = 600, 5900      # Kreisais apakšējais stūris
        x4, y4 = 7000, 5900     # Apakšējais labais stūris
        distance_m = 150

        # 🟦 Синие линии
        blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

        blue_line_thickness = 3

    else:
        raise ValueError("Unknown video type")

    return (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
                blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
                blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
                blue_line_thickness)