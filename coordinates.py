def get_coordinates(video_path):
# Coordinates of the frame and blue lines for different videos
    if "50kmh_mugur_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 4400, 2900      # Augšējais labais stūris
        x2, y2 = 4000, 2900     # Augšējais kreisais stūris
        x3, y3 = 7700, 6300     # Kreisais apakšējais stūris
        x4, y4 = 11500, 5000    # Apakšējais labais stūris
        distance_m = 65

        # blue
        blue_x1_top, blue_y1_top = 4100, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 4750, 3020           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5900     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10500, 4700    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_prieksa_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 5200, 3000     # Augšējais labais stūris
        x2, y2 = 4900, 3000     # Augšējais kreisais stūris
        x3, y3 = 7950, 5500     # Kreisais apakšējais stūris
        x4, y4 = 11000, 4800    # Apakšējais labais stūris
        distance_m =65

        # blue
        blue_x1_top, blue_y1_top = 4950, 3100           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5550, 3075           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5500     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 11000, 4750    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_mugur_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 4950, 2850     # Augšējais labais stūris
        x2, y2 = 3950, 2850     # Augšējais kreisais stūris
        x3, y3 = 7300, 5900     # Kreisais apakšējais stūris
        x4, y4 = 10400, 4550     # Apakšējais labais stūris
        distance_m = 65

        # blue
        blue_x1_top, blue_y1_top = 5000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 5000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 5250    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_prieksa_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 5150, 3000   # Augšējais labais stūris
        x2, y2 = 4750, 3000   # Augšējais kreisais stūris
        x3, y3 = 9000, 6500   # Kreisais apakšējais stūris
        x4, y4 = 11500, 4900  # Apakšējais labais stūris
        distance_m = 50

        # blue
        blue_x1_top, blue_y1_top = 4850, 3100         # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5550, 3075         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 8200, 6375   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 11000, 4750  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6000, 2900     # Augšējais labais stūris
        x2, y2 = 5650, 2900     # Augšējais kreisais stūris
        x3, y3 = 400, 5800      # Kreisais apakšējais stūris
        x4, y4 = 6900, 6000     # Apakšējais labais stūris
        distance_m = 45

        # blue
        blue_x1_top, blue_y1_top = 4900, 3200           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6100, 3200           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 900, 5550     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6900, 5700    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6400, 3200     # Augšējais labais stūris
        x2, y2 = 5500, 3200     # Augšējais Kreisais stūris
        x3, y3 = 400, 5700     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6200    # labais apakšējais stūris
        distance_m =45

        # blue
        blue_x1_top, blue_y1_top = 5300, 4300           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6400, 4300           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 900, 5500     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6500, 5900    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "80kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6400, 3100     # Augšējais labais stūris
        x2, y2 = 5500, 3100     # Augšējais Kreisais stūris
        x3, y3 = 400, 5700     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6200    # labais apakšējais stūris
        distance_m =45

        # blue
        blue_x1_top, blue_y1_top = 5000, 3350           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6400, 3400           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 850, 5400     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6500, 5800    # Apakšējais labais stūris

        blue_line_thickness = 3

    else:
        raise ValueError("Unknown video type")

    return (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
                blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
                blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
                blue_line_thickness)