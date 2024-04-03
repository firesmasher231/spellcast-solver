import mss.tools

with mss.mss() as sct:
    # The screen part to capture
    monitor = {"top": 400, "left": 1000, "width": 550, "height": 550}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    ## save sct_img to file

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

    sct.shot()
