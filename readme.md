PyDanmaku
	A bullet hell shooting game

How to run
	run main program:
		main.py
	train ai:
		1.	main.py
		2.	.\ai\aiTrain.py	(run in ide)
	test ai:
		1.	main.py
		2.	.\ai\runwinner.py	(run in ide)

Libraries
	Pygame(https://www.pygame.org/)
		install: python3 -m pip install -U pygame --user
	BulletML(https://pypi.org/project/python-bulletml/)
		install: git clone http://git.yukkurigames.com/python-bulletml.git
	neat-python(https://neat-python.readthedocs.io/en/latest/)
		install: pip install neat-python
	PAdLib(https://www.pygame.org/project-Pygame+Advance+Graphics+Library-660-1274.html)
		install: included

Shotcut
	change ".\sprites.py" row 386 "self.damage(1)" to "self.damage(100)"