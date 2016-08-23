import pysynth

set1 = [['g#3',4],['f#3',4],['e3',4],['b2',2],]
set2 = [['e3',4],['g#3',4],['f#3',4],['b2',2],]
set3 = [['e3',4],['f#3',4],['g#3',4],['e3',2],]
set4 = [['g#3',4],['e3',4],['f#3',4],['b2',2],]
set5 = [['b2',4],['f#3',4],['g#3',4],['e3',2],]
rest = [['r',4]]

quarter1 = set1
quarter2 = set2 + set3
quarter3 = set4 + set5 + set1
quarter4 = set2 + set3 + set4 + set5  # + rest

print
print "Creating chime files... (this might take about a minute)"
print

# create the hour chimes: h1mono.wav, h2mono.wav, ...
on_hour = []
for i in range(1,10):
    on_hour.append(['e2',-2])
    pysynth.make_wav(on_hour, bpm = 60, fn = "h0" + str(i) + "mono.wav")
for j in range(10,13):
    on_hour.append(['e2',-2])
    pysynth.make_wav(on_hour, bpm = 60, fn= "h" + str(j) + "mono.wav")

# quarter hour
pysynth.make_wav(quarter1, bpm = 60, fn = "q1mono.wav")

# half hour
pysynth.make_wav(quarter2, bpm = 60, fn = "q2mono.wav")

# three-quarter hour
pysynth.make_wav(quarter3, bpm = 60, fn = "q3mono.wav")

# full hour
pysynth.make_wav(quarter4, bpm = 60, fn = "q4mono.wav")
'''
# make the quarters in stereo
for i in range(1,5):
    pysynth.mix_files("q" + str(i) + "mono.wav", "q" + str(i) + "mono.wav",\
            "q" + str(i) + "stereo.wav")

# make the hours in stereo
for i in range(1, 13):
    pysynth.mix_files("h" + str(i) + "mono.wav", "h" + str(i) + "mono.wav",\
            "h" + str(i) + "stereo.wav")
'''
print "Finished"
