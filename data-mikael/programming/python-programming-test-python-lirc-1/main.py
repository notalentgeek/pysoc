import lirc

sockid = lirc.init("pysoc")
print(lirc.nextcode())
print("a remote button have just pressed")
lirc.deinit()