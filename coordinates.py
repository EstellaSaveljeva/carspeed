def get_coordinates(video_path):
# Coordinates of the frame and blue lines for different videos
    if "50kmh_mugur_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 4500, 2850      # Augšējais labais stūris
        x2, y2 = 3850, 2850     # Augšējais kreisais stūris
        x3, y3 = 7600, 7000     # Kreisais apakšējais stūris
        x4, y4 = 13500, 4800    # Apakšējais labais stūris
        distance_m = 60

        # blue
        blue_x1_top, blue_y1_top = 4000, 3050           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5300, 3020           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 6650, 6200     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 11500, 4600    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_prieksa_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 5100, 2900     # Augšējais labais stūris
        x2, y2 = 4800, 2900     # Augšējais kreisais stūris
        x3, y3 = 8200, 7000     # Kreisais apakšējais stūris
        x4, y4 = 12000, 4800    # Apakšējais labais stūris
        distance_m =60

        # blue
        blue_x1_top, blue_y1_top = 4900, 3090           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5900, 3050           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7400, 6300     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 11500, 4500    # Apakšējais labais stūris
        blue_line_thickness = 3

    elif "70kmh_mugur_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 4700, 2900   # Augšējais labais stūris
        x2, y2 = 4100, 2900   # Augšējais kreisais stūris
        x3, y3 = 8300, 6450   # Kreisais apakšējais stūris
        x4, y4 = 12000, 4300  # Apakšējais labais stūris
        distance_m = 60

        # blue
        blue_x1_top, blue_y1_top = 4300, 3085         # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5450, 3045         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7650, 5850   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10950, 4150  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_prieksa_jaunolaine" in video_path.lower():
        # red
        x1, y1 = 5125, 2800   # Augšējais labais stūris
        x2, y2 = 4500, 2800   # Augšējais kreisais stūris
        x3, y3 = 8500, 6500   # Kreisais apakšējais stūris
        x4, y4 = 13000, 4700  # Apakšējais labais stūris
        distance_m = 50

        # blue
        blue_x1_top, blue_y1_top = 4800, 3100         # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6150, 3050         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 7350, 5400   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 10900, 4150  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6000, 2850     # Augšējais labais stūris
        x2, y2 = 5450, 2850     # Augšējais kreisais stūris
        x3, y3 = -3000, 6800      # Kreisais apakšējais stūris
        x4, y4 = 6900, 7000     # Apakšējais labais stūris
        # distance_m = 40
        distance_m = 35

        # blue
        blue_x1_top, blue_y1_top = 4800, 3100          # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6100, 3200           # Augšējais labais stūris
        # blue_x1_bottom, blue_y1_bottom = -100, 5690     # Kreisais apakšējais stūris
        # blue_x2_bottom, blue_y2_bottom = 6900, 6040 
        # 51,74    # Apakšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 2000, 4290     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6900, 4640   # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6400, 3000     # Augšējais labais stūris
        x2, y2 = 5700, 3000     # Augšējais Kreisais stūris
        x3, y3 = -300, 6000     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6500    # labais apakšējais stūris
        distance_m =35

        # blue
        blue_x1_top, blue_y1_top = 5000, 3300           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6400, 3300           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 2400, 4300     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6500, 4700    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "80kmh_ropazi" in video_path.lower():
        # red
        x1, y1 = 6400, 3100     # Augšējais labais stūris
        x2, y2 = 5500, 3100     # Augšējais Kreisais stūris
        x3, y3 = -1000, 5700     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6800    # labais apakšējais stūris
        distance_m =35

        # blue
        blue_x1_top, blue_y1_top = 4800, 3350           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 6400, 3350           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1100, 4900     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6500, 5300    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_2k_24fps" in video_path.lower():
        # red
        x1, y1 = 2700, 1400   # Augšējais labais stūris
        x2, y2 = 2600, 1400   # Augšējais kreisais stūris
        x3, y3 = 50, 2500   # Kreisais apakšējais stūris
        x4, y4 = 3000, 2800  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2100, 1610        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2770, 1640          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 630, 2250   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 2910, 2400  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_2k_48fps" in video_path.lower():
        # red
        x1, y1 = 2850, 1300   # Augšējais labais stūris
        x2, y2 = 2750, 1300   # Augšējais kreisais stūris
        x3, y3 = 50, 2500   # Kreisais apakšējais stūris
        x4, y4 = 3200, 3000  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2250, 1515        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2870, 1545          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 680, 2000   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 3000, 2250  # Apakšējais labais stūris

        blue_line_thickness = 3
    
    elif "50kmh_2k_60fps" in video_path.lower():
        # red
        x1, y1 = 2870, 1400   # Augšējais labais stūris
        x2, y2 = 2750, 1400   # Augšējais kreisais stūris
        x3, y3 = 50, 2500   # Kreisais apakšējais stūris
        x4, y4 = 3300, 3100  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2250, 1600        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2910, 1630          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 890, 2100   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 3030, 2370  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_4k_24fps" in video_path.lower():
        # red
        x1, y1 = 5770, 2800     # Augšējais labais stūris
        x2, y2 = 5500, 2800     # Augšējais Kreisais stūris
        x3, y3 = -300, 5800     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6300    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4700, 3200           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5850, 3250           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 2400, 4400     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6330, 4700    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_4k_48fps" in video_path.lower():
        # red
        x1, y1 = 5820, 2900     # Augšējais labais stūris
        x2, y2 = 5500, 2900     # Augšējais Kreisais stūris
        x3, y3 = -300, 5800     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6300    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4620, 3400           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5900, 3450           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 2400, 4550     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6330, 4850    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "50kmh_4k_60fps" in video_path.lower():
        # red
        x1, y1 = 5720, 2700     # Augšējais labais stūris
        x2, y2 = 5400, 2700     # Augšējais Kreisais stūris
        x3, y3 = -300, 5800     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6300    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4500, 3180           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5840, 3230           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 2130, 4550     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6330, 4850    # Apakšējais labais stūris

        blue_line_thickness = 3
    elif "50kmh_1080_24fps" in video_path.lower():
        # red
        x1, y1 = 1375, 750  # Augšējais labais stūris
        x2, y2 = 1200, 750   # Augšējais kreisais stūris
        x3, y3 = -100, 1400   # Kreisais apakšējais stūris
        x4, y4 = 1600, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 980, 860        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1420, 870         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 300, 1200   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1550, 1240  # Apakšējais labais stūris

        blue_line_thickness = 2

    elif "50kmh_1080_48fps" in video_path.lower():
        # red
        x1, y1 = 1385, 750  # Augšējais labais stūris
        x2, y2 = 1300, 750   # Augšējais kreisais stūris
        x3, y3 = -100, 1400   # Kreisais apakšējais stūris
        x4, y4 = 1600, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 1045, 860        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1420, 870         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 420, 1140   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1520, 1180  # Apakšējais labais stūris

        blue_line_thickness = 2
    
    elif "50kmh_1080_60fps" in video_path.lower():
        # red
        x1, y1 = 1460, 750  # Augšējais labais stūris
        x2, y2 = 1380, 750   # Augšējais kreisais stūris
        x3, y3 = -200, 1400   # Kreisais apakšējais stūris
        x4, y4 = 1650, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 1145, 845        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1480, 855         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 420, 1140   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1550, 1180  # Apakšējais labais stūris

        blue_line_thickness = 2
    elif "50kmh_1080_60fps_2car" in video_path.lower():
        # red
        x1, y1 = 1460, 750  # Augšējais labais stūris
        x2, y2 = 1380, 750   # Augšējais kreisais stūris
        x3, y3 = -200, 1400   # Kreisais apakšējais stūris
        x4, y4 = 1650, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 1145, 845        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1480, 855         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 420, 1140   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1550, 1180  # Apakšējais labais stūris

        blue_line_thickness = 2

    elif "60kmh_2k_24fps" in video_path.lower():
        # red
        x1, y1 = 2700, 1100   # Augšējais labais stūris
        x2, y2 = 2550, 1100   # Augšējais kreisais stūris
        x3, y3 = -500, 2400   # Kreisais apakšējais stūris
        x4, y4 = 3200, 3000  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2050, 1310        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2800, 1340          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 670, 1920   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 3000, 2170  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "60kmh_2k_48fps" in video_path.lower():
        # red
        x1, y1 = 2710, 1135   # Augšējais labais stūris
        x2, y2 = 2550, 1135   # Augšējais kreisais stūris
        x3, y3 = -500, 2400   # Kreisais apakšējais stūris
        x4, y4 = 3200, 3000  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2000, 1363        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2800, 1393          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 620, 1940   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 3000, 2190  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "60kmh_2k_60fps" in video_path.lower():
        # red
        x1, y1 = 2710, 1135   # Augšējais labais stūris
        x2, y2 = 2550, 1135   # Augšējais kreisais stūris
        x3, y3 = -500, 2400   # Kreisais apakšējais stūris
        x4, y4 = 3200, 3000  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 2050, 1305        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 2800, 1355          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 620, 1940   # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 3000, 2190  # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_4k_24fps" in video_path.lower():
        # red
        x1, y1 = 5650, 2450     # Augšējais labais stūris
        x2, y2 = 5200, 2450     # Augšējais Kreisais stūris
        x3, y3 = -1000, 5200     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6100    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4280, 2875           # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5840, 2925           # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1000, 4320     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6310, 4650    # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_4k_48fps" in video_path.lower():
        # red
        x1, y1 = 5500, 2350     # Augšējais labais stūris
        x2, y2 = 5100, 2350     # Augšējais Kreisais stūris
        x3, y3 = -1000, 5100     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 6000    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4260, 2750          # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5760, 2850          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1130, 4000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6260, 4460   # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_4k_60fps" in video_path.lower():
        # red
        x1, y1 = 5700, 2350     # Augšējais labais stūris
        x2, y2 = 5300, 2350     # Augšējais Kreisais stūris
        x3, y3 = -1000, 4900     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 5800    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4260, 2755          # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5800, 2855          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1130, 4000     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6260, 4460   # Apakšējais labais stūris

        blue_line_thickness = 3

    elif "70kmh_1080_24fps" in video_path.lower():
        # red
        x1, y1 = 1450, 600  # Augšējais labais stūris
        x2, y2 = 1300, 600   # Augšējais kreisais stūris
        x3, y3 = -500, 1200   # Kreisais apakšējais stūris
        x4, y4 = 1600, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 950, 710        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1460, 750         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 200, 950  # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1540, 1150  # Apakšējais labais stūris

        blue_line_thickness = 2
    
    elif "70kmh_1080_48fps" in video_path.lower():
        # red
        x1, y1 = 1450, 550  # Augšējais labais stūris
        x2, y2 = 1330, 550   # Augšējais kreisais stūris
        x3, y3 = -500, 1200   # Kreisais apakšējais stūris
        x4, y4 = 1600, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 970, 670        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1460, 710         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 250, 880  # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1540, 1080  # Apakšējais labais stūris

        blue_line_thickness = 2

    elif "70kmh_1080_60fps" in video_path.lower():
        # red
        x1, y1 = 1450, 550  # Augšējais labais stūris
        x2, y2 = 1330, 550   # Augšējais kreisais stūris
        x3, y3 = -500, 1200   # Kreisais apakšējais stūris
        x4, y4 = 1600, 1500  # Apakšējais labais stūris
        distance_m = 23

        # blue
        blue_x1_top, blue_y1_top = 970, 660        # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 1460, 700         # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 250, 800  # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 1540, 950  # Apakšējais labais stūris

        blue_line_thickness = 2

    elif "wv_4k_48fps" in video_path.lower():
        # red
        x1, y1 = 5700, 2750     # Augšējais labais stūris
        x2, y2 = 5300, 2750     # Augšējais Kreisais stūris
        x3, y3 = -1000, 4900     # Apakšējais Kreisais stūris
        x4, y4 = 6600, 5800    # labais apakšējais stūris
        distance_m =23

        # blue
        blue_x1_top, blue_y1_top = 4260, 3250          # Augšējais kreisais stūris
        blue_x2_top, blue_y2_top = 5800, 3350          # Augšējais labais stūris
        blue_x1_bottom, blue_y1_bottom = 1130, 4100     # Kreisais apakšējais stūris
        blue_x2_bottom, blue_y2_bottom = 6260, 4560   # Apakšējais labais stūris

        blue_line_thickness = 3 

    else:
        raise ValueError("Unknown video type")

    return (x1, y1, x2, y2, x3, y3, x4, y4, distance_m,
                blue_x1_top, blue_y1_top, blue_x2_top, blue_y2_top,
                blue_x1_bottom, blue_y1_bottom, blue_x2_bottom, blue_y2_bottom,
                blue_line_thickness)