

def test_cron():
    print("working?")
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()