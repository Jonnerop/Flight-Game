# Old eventfunction
def add_events():
    # bad choices 1
    bc1 = (("Make a sharp maneuver to avoid birds. This sudden move might damage cargo.", "money -3000"),
           ("Maintain course and hope the birds pass safely.", "money 0"),
           ("Brace for potential bird strike. Birds collide with the plane, causing some damage", "karma -5"))
    # bad event 1
    be1 = ("Mid-flight, you spot a massive flock of birds rapidly approaching. "
           "The cockpit alarms blare, warning of collision risk. You have three options")
    # kun ei ole valintoja, valinta 1 muodostetaan näin
    bc2 = ("", "money -2000")
    be2 = ("You have trouble communicating with people in and around the airport. They just simply don’t "
           "understand you or refuse to do so. You’re pretty sure you’ve been charged extra for just about everything.")

    bc3 = ((
           "Push the throttle and ascend to smoother air above the storm. Turbulence lessens and you find respite above the dark clouds.",
           "money 0"),
           (
           "Consult air traffic control to find a path around the storm. You turn sharply off-course to avoid the worst of the tempest, flying a longer route",
           "rounds -0"),
           (
           "Decide to maintain your current altitude and power through the storm, expecting to emerge on the other side unscathed. \nThe turbulence is strong, and your aircraft is bound to take damage.",
           "money -5000"))
    be3 = ("In the middle of your flight, a menacing thunderstorm surrounds you. The aircraft shakes as the heavy rain"
           " and lightning creates an intimidating atmosphere. You have three choices:")

    bc4 = ("", "money -6000")
    be4 = (
        "In poor visibility conditions, you miss the runway landing and crash into an area nearby. The impact is devastating, resulting in a damaged airplane and cargo.")

    bc5 = ("", "money -3000")
    be5 = (
        "Once again you decide to buy some pastries from the cantina. With a hop, skip and a jump you approach the counter \nwhen you realise you can't find your wallet anywhere. Luckily you stored only some of your money there.")

    # good event
    gc1 = ((
           "You decide to inform the shipping company about the valuable cargo. They may have specific instructions on how to handle it, \nand you want to make sure it's delivered safely and securely.",
           "money +4000"),
           (
           "You take measures to secure the valuable cargo within the airplane, making sure it’s well-protected and will reach \nits destination in one piece.",
           "karma +1"),
           (
           "You decide to use the cargo for a good cause. Whether it’s a charitable donation or contributing to a worthy organization, \nyou choose to turn the valuable cargo into a means of making a positive impact.",
           "karma +5"))
    ge1 = (
        "In the middle of the flight, while checking the cargo hold, you come across an unexpected discovery, a valuable and \nrare item among the cargo. How you proceed offers three choices:")

    gc2 = ("", "money +3000")
    ge2 = (
        "'Unfortunately', your distant wealthy relative has passed away, and you have the opportunity to inherit their assets. \nThis unexpected inheritance is very much welcome in your almost empty bank account.")

    gc3 = ("", "rounds +0")
    ge3 = (
        "Flying your cargo plane, you were captivated by the breathtaking beauty below. The serene nature, rolling hills, \nand vivid sunset colours made you forget everything else, and time seemed to vanish as you flew on.")

    gc4 = ("", "money +5000")
    ge4 = (
        "The wind blows a lottery ticket right in front of you. To your amazement, it turned out to be a winning ticket.")

    gc5 = ("", "money +1500")
    ge5 = ("You win second place in a beauty contest. Huh?")

    # neutral event
    nc1 = ((
           "You decide to inflate the rubber chicken even further, thinking it might make a more competent pilot if it's larger. \nThe chicken inflates even further, and its control of the plane becomes even more erratic.",
           "karma +10"),
           (
           "You engage in a detailed, over the top, and comical training session with the rubber chicken, making use of a chalkboard \nand pointer. You are hoping for a miraculous improvement in its performance.",
           "karma +5"),
           (
           "You challenge the rubber chicken to a dance-off, with the winner earning the control of the plane. A ridiculous dance battle \nunfolds in the cockpit, with exaggerated dance moves and music blasting in the background.",
           "karma +15"))
    ne1 = (
        "You spot the automatic pilot controls, and in a moment of absurdity, decide to engage the autopilot. However, \nto your astonishment, the autopilot is not what you anticipated. It's an oversized rubber chicken wearing a pilot’s uniform, and it’s now in control of the plane. \nYou have three choices:")

    nc2 = (("I'm on a tight schedule, surely the kid will be fine.", "karma -15"),
           ("I mean it’s a big airport, someone will find them soon.", "karma -10"),
           ("Stranger be damned. Let’s figure out how we can help this child", "karma +10"))
    ne2 = (
        "The Stranger calls you and it’s not a polite call, you’re late. Hurriedly you prepare everything to take flight \nas soon as possible when suddenly you see a lone child wandering about. The child is teary eyed and clearly lost. What do you do?")

    nc3 = (("I do. And don’t call me Shirley.", "karma +0"),
           ("As long as Leslie Nielsen won’t show up we should be golden.", "karma +0"),
           ("What the hell are you on about?", "karma +0"))
    ne3 = (
        "You feel very weird after eating a fish dinner at the airport cantina. Reality starts to shift and you feel almost \nas if you were in a 1980’s comedy film somehow related to airplanes. Surely you know how to proceed?")

    nc4 = ("", "rounds -0")
    ne4 = (
        "As the freighter airplane is headed for its destination, suddenly, a large eagle struck the plane’s wing with \ngreat force. As a result of the impact, the plane’s engine began to show signs of disruption. Upon landing you need to do an inspection immediately.")

    nc5 = ("", "charge -5")
    ne5 = (
        "During the freighter airplane’s flight, an unexpected power outage occurs, shutting down all systems. This causes \nyou to panic and requires you to take quick actions to resolve the electrical issues and safely navigate the airplane.")

    nc6 = ("", "money -4000")
    ne6 = (
        "After landing the freighter airplane at your destination, you begin to do your regular check up on the cargo. \nYou realize something terrible has happened. The cargo has dislodged during the flight and the valuable cargo has been damaged. To the best of your ability, you try to salvage what is left of the undamaged cargo, working quickly to minimize further losses.")

    nc7 = ("", "rounds -0")
    ne7 = (
        "During your flight, a technical glitch led to data loss in the aircraft’s navigation system. This has caused a delay \nas you cautiously navigated without the needed information. This caused a significant delay in your arrival which led to monetary loss and impediment in your schedule.")

    events = {"bad": ((be1, bc1), (be2, bc2), (be3, bc3), (be4, bc4), (be5, bc5)),
              "good": ((ge1, gc1), (ge2, gc2), (ge3, gc3), (ge4, gc4), (ge5, gc5)),
              "neutral": ((ne1, nc1), (ne2, nc2), (ne3, nc3), (ne4, nc4), (ne5, nc5), (ne6, nc6), (ne7, nc7))}
    return events

# Old first event function
# def first_event():
# return firstevent


firstevent = '''You are preparing for your first flight and decide to celebrate the occasion with some pastries from the 
airport cantina. Halfway there you remember your less than stellar monetary predicament. You almost turned back when you 
remembered the premium the Stranger had handed you for initial expenses, except they’re not in any currency you’re 
familiar with. 

You call the Stranger and he explains they’re JETT-coins and not to worry as all airport services will accept them. 
Begrudgingly you decide to test that out as you’re not quite sure if you trust him yet. Surprisingly the transaction 
went without a hitch and you walked back to the hangar with your tasty prize, even more confused than you were before.'''
