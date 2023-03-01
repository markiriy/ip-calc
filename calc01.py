import pygame as pg

file = open('calc.txt', 'w')

def main():
    def dtb(n):
        return format(n, '08b')

    def cidr_to_subnet(CIDR):
        counter = 0
        subnet = []
        while (CIDR > 8):
            CIDR = CIDR - 8
            counter += 1
        for i in range(4):
            if i < counter:
                subnet.append(255)
            elif i == counter:
                subnet.append(256 - pow(2, (8 - CIDR)))
            else:
                subnet.append(0)
        return subnet

    kit = "kit.png"
    music = "песенка.mp3"

    pg.init()
    screen = pg.display.set_mode((640, 480))
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    COLOR_ACTIVE = pg.Color('dodgerblue2')
    FONT = pg.font.SysFont("monospace", 20)
    txtfont = pg.font.SysFont("monospace", 16)

    pg.mixer.init()
    pg.mixer.music.load(music)
    pg.mixer.music.play()
    pg.event.wait()

    network = []
    mask = []
    idnet = []
    bdadd = []
    firstid = ['']
    lastid = ['']
    tothosts = []

    class InputBox:

        def __init__(self, x, y, w, h, text=''):
            self.rect = pg.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.txt_surface = FONT.render(text, True, self.color)
            self.active = False

        def handle_event(self, event):
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            if event.type == pg.KEYDOWN:
                if self.active:
                    if event.key == pg.K_RETURN:
                        network.append(self.text)
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.txt_surface = FONT.render(self.text, True, self.color)
            if len(network) == 2:
                ip = []
                check_ip = True
                while check_ip:
                    try:
                        ip = list(map(int, network[0].split('.')))
                        check_ip = False
                        if len(ip) != 4:
                            print("Error: IP Address supported format X.X.X.X")
                            exit(0)
                            break
                        for i in ip:
                            if i > 255:
                                print("Error: IP Address Range: (0-255)")
                                exit(0)
                                break
                        continue
                    except ValueError:
                        print("Error: Only integers are allowed")
                        exit(0)
                        break
                    except KeyboardInterrupt:
                        print("IP Calculator has been terminated.")
                        exit(0)
                    except:
                        print("An error has occurred.")
                        exit(0)
                        break

                subnet = []
                check_subnet = True
                while (check_subnet):
                    try:
                        CIDR = network[1]
                        if CIDR[0] == '/':
                            CIDR = int(CIDR[1:])
                            if not CIDR in range(8, 31):
                                print("Invalid shorthand notation. Must be in the range of 8-30.")
                                exit(0)
                                break
                            else:
                                subnet = cidr_to_subnet(CIDR)
                                check_subnet = False
                        else:
                            subnet = list(map(int, CIDR.split('.')))
                            if subnet[0] != 255:
                                print("Invalid subnet mask. The lowest allowed mask must be 255.0.0.0")
                                exit(0)
                                continue
                            check_subnet = False
                        if len(subnet) != 4:
                            print("Error: Subnet Mask supported format X.X.X.X")
                            exit(0)
                            break
                        for j in subnet[1:]:
                            if j > 255:
                                print("Error: Subnet Mask Range: (0-255)")
                                exit(0)
                                break
                            if '01' in dtb(j):
                                print("Error: Invalid subnet mask, it must contain continous ones.")
                                exit(0)
                                break
                        continue
                    except ValueError:
                        print("Error: Only integers are allowed.")
                        exit(0)
                        break
                    except KeyboardInterrupt:
                        print()
                        print("IP Calculator has been terminated.")
                        exit(0)
                    except:
                        print("An error has occurred.")
                        exit(0)
                        break

                print(f"Введенные данные: АДРЕС - {'.'.join(map(str, ip))}, МАСКА - {'.'.join(map(str,subnet))}")
                subnet_ones = 0
                t_no_hosts = 0
                network_id = []
                broadcast_address = [0, 0, 0, 0]

                for i in range(4):
                    subnet_ones = subnet_ones + len(dtb(subnet[i]).strip('0'))
                    network_id.append(int(ip[i]) & int(subnet[i]))
                    if subnet[i] == 255:
                        broadcast_address[i] = network_id[i]
                    else:
                        broadcast_address[i] = 255 - subnet[i] + network_id[i]

                mask.append(str(subnet_ones))
                idnet.append(network_id[0]), idnet.append(network_id[1]), idnet.append(network_id[2]), idnet.append(network_id[3])

                bdadd.append('.'.join(map(str, broadcast_address)))
                t_no_hosts = pow(2, 32 - subnet_ones) - (2)
                first_id = network_id.copy()
                first_id[3] += 1

                firstid.append(str(first_id[0])), firstid.append(str(first_id[1])), firstid.append(str(first_id[2])), firstid.append(str(first_id[3]))

                last_address = broadcast_address.copy()
                last_address[3] -= 1

                lastid.append(str(last_address[0])), lastid.append(str(last_address[1])), lastid.append(str(last_address[2])), lastid.append(str(last_address[3]))
                lastid.pop(0)
                firstid.pop(0)

                tothosts.append(t_no_hosts)

                file.write("----------------------------------\n")
                file.write(f"CIDR: /{subnet_ones}\n")
                file.write(f"Network ID: {'.'.join(map(str, network_id))}\n")
                file.write(f"First Host Address: {'.'.join(map(str, first_id))}\n")
                file.write(f"Last Host Address: {'.'.join(map(str, last_address))}\n")
                file.write(f"Broadcast Address: {'.'.join(map(str, broadcast_address))}\n")
                file.write(f"Total number of Hosts = {str(t_no_hosts)}\n")

                network.clear()




        def update(self):
            # Resize the box if the text is too long.
            width = max(200, self.txt_surface.get_width()+10)
            self.rect.w = width

        def draw(self, screen):
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pg.draw.rect(screen, self.color, self.rect, 2)

    clock = pg.time.Clock()
    input_box1 = InputBox(130, 80, 140, 32)
    input_box2 = InputBox(130, 150, 140, 32)
    inforect = pg.Rect(20, 200, 600, 220)
    input_boxes = [input_box1, input_box2]
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.draw.rect(screen, COLOR_INACTIVE, inforect, 2)

        textip = FONT.render("IP-адрес:", True, (255, 255, 255))
        screen.blit(textip, (15, 85))

        textmask = FONT.render("Маска:", True, (255, 255, 255))
        screen.blit(textmask, (50, 155))

        ipcalc = FONT.render("IP CALCULATOR", True, (255, 255, 255))
        screen.blit(ipcalc, (230, 18))

        cato = pg.image.load(kit).convert_alpha()
        cato = pg.transform.scale(cato, (250, 130))
        rec = cato.get_rect()
        rec.x = 370
        rec.y = 53
        screen.blit(cato, rec)

        if len(mask) == 1:
            label = txtfont.render(f"CIDR: /{mask[0]}", True, (255, 255, 255))
            screen.blit(label, (40, 220))

            idlabel = '.'.join(map(str, idnet))
            label2 = txtfont.render("Network ID: " + str(idlabel), True, (255, 255, 255))
            screen.blit(label2, (40, 240))

            hostlabel = '.'.join(map(str, firstid))
            label3 = txtfont.render("First Host Address: " + str(hostlabel), True, (255, 255, 255))
            screen.blit(label3, (40, 260))

            lhostlabel = '.'.join(map(str, lastid))
            label4 = txtfont.render("Last Host Address: " + str(lhostlabel), True, (255, 255, 255))
            screen.blit(label4, (40, 280))

            brlabel = '.'.join(map(str, bdadd))
            label5 = txtfont.render("Broadcast Address: " + str(brlabel), True, (255, 255, 255))
            screen.blit(label5, (40, 300))

            label6 = txtfont.render("Total number of Hosts = " + str(tothosts[0]), True, (255, 255, 255))
            screen.blit(label6, (40, 320))

            veder = txtfont.render("Ведерникова проходит приблизительно 234000 шагов в месяц", True, (255, 255, 255))
            screen.blit(veder, (40, 360))

        elif len(mask) > 1:
            mask.pop(0)
            del idnet[4:7]
            bdadd.pop(0)
            del firstid[4:7]
            del lastid[4:7]
            tothosts.pop(0)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()

file.close()
