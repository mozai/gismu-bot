#!/usr/bin/env python
import re, string, random

class Eliza:
  """
  The original Eliza is by Joseph Weizenbaum
  This is from a version in BASIC by Jeff Shrager,
  edited by Bob Anderson for Creative Computing Magazine.
  rewritten into Python by Moses Moore.
  TODO: converting pronouns and conjugates between first/second person
  """
  brain = {
    "can you":
      ["Don't you believe I can*"
      ,"Perhaps you would like to be able to*"
      ,"You want me to be able to*"
      ],
    "can i":
      ["Perhaps you don't want to*"
      ,"Do you want to be able to*"
      ],
    "you are":
      ["What makes you think I am*"
      ,"Does it please you to believe that I am*"
      ,"Do you sometimes wish you were*"
      ],
    "youre": "you are",
    "i dont":
      ["Don't you really*"
      ,"Why don't you*"
      ,"Do you wish to be able to*"
      ,"Does that trouble you?"
      ],
    "i feel":
      ["Tell me more about such feelings."
      ,"Do you often feel*"
      ,"Do you enjoy feeling*"
      ],
    "why dont you":
      ["Do you really believe I don't*"
      ,"Perhaps in good time I will*"
      ,"Do you want me to*"
      ],
    "why cant i":
      ["Do you think you should be able to*"
      ,"Why can't you*"
      ],
    "are you":
      ["Why are you interested in whether or not I am*"
      ,"Would you prefer if I were not*"
      ,"Perhaps in your fantasies I am*"
      ],
    "i cant":
      ["How do you know you can't*"
      ,"Have you tried?"
      ,"Perhaps you can now*"
      ],
    "i am":
      ["Did you come to me because you are*"
      ,"How long have you been*"
      ,"Do you believe it is normal to be*"
      ,"Do you enjoy being*"
      ],
    "im": "i am",
    "you":
      ["We were discussing you -- not me."
      ,"Oh, I*"
      ,"You're not really talking about me, are you?"
      ],
    "i want":
      ["What would it mean if you got*"
      ,"Why do you want*"
      ,"Suppose you soon got*"
      ,"What if you never got*"
      ,"I sometimes also want*"
      ],
    "i wish" : "i want",
    "what":
      ["Why do you ask?"
      ,"Does that question interest you?"
      ,"What answer would please you the most?"
      ,"What do you think?"
      ,"Are such questions on your mind often?"
      ,"What is it you really want to know?"
      ,"Have you asked anyone else?"
      ,"Have you asked such questions before?"
      ,"What else comes to mind when you ask that?"
      ],
    "how":   "what",
    "who":   "what",
    "where": "what",
    "when":  "what",
    "why":   "what",
    "name":
      ["Names don't interest me."
      ,"I don't care about names. Please go on."
      ],
    "cause":
      ["Is that the real reason?"
      ,"Don't any other reasons come to mind?"
      ,"Does that reason explain anything else?"
      ,"what other eason might there be?"
      ],
    "sorry":
      ["Please don't apologize."
      ,"Apologies are not necessary."
      ,"What feelings do you get when you apologize?"
      ,"Don't be so defensive!"
      ],
    "dream":
      ["What does that dream suggest to you?"
      ,"Do you dream often?"
      ,"What persons appear in your dreams?"
      ,"Are you disturbed by your dreams?"
      ],
    "hello":
      ["How do you do... Please state your problem."
      ],
    "hi": "hello",
    "maybe":
      ["You don't seem quite certain."
      ,"why the uncertain tone?"
      ,"Can't you be more positive?"
      ,"You aren't sure?"
      ,"Don't you know?"
      ],
    "no":
      ["Are you saying that just to be contrary?"
      ,"You are being a bit negative."
      ,"Why not?"
      ,"Are you sure?"
      ,"Why no?"
      ],
    "your":
      ["Why are you concerned about my*"
      ,"What about your own*"
      ],
    "always":
      ["Can you think of a specific example?"
      ,"When?"
      ,"What are you thinking of?"
      ,"Really, always?"
      ],
    "think":
      ["Do you really think so?"
      ,"But you are not sure you*"
      ,"Do you doubt you*"
      ],
    "alike":
      ["In what way?"
      ,"What resemblance do you see?"
      ,"What does the similarity suggest to you?"
      ,"What other connections do you see?"
      ,"Could there really be some connection?"
      ,"How?"
      ],
    "yes":
      ["You seem quite positive."
      ,"Are you sure?"
      ,"I see."
      ,"I understand."
      ],
    "friend":
      ["Why do you bring up the topic of friends?"
      ,"Do your friends worry you?"
      ,"Do your friends pick on you?"
      ,"Are you sure of your friends?"
      ,"Do you impose on your friends?"
      ,"Perhaps your love for your friends worries you?"
      ],
    "computer":
      ["Do computers worry you?"
      ,"Are you talking about me in particular?"
      ,"Are you frightened by machines?"
      ,"Why do you mention computers?"
      ,"What do you think computers have to do with your problems?"
      ,"Don't you think computers can help people?"
      ,"What is it about machines that worries you?"
      ],
    "":
      ["Say, do you have any psychological problems?"
      ,"What does that suggest to you?"
      ,"I see."
      ,"I'm not sure I understand you fully."
      ,"Come come, eucidate your thoughts"
      ,"Can you elaborate on that?"
      ,"That is quite interesting."
      ]
  }
  conjugates = {
    'are':'am', 'am':'are', 'where':'was', 'was':'were', 'you':'I',
    'i':'you', 'your':'my', 'my':'your', 'ive':"you've", 'youve':"I've",
    'im':"you're", 'youre':"I'm"
  }

  def input(self, query=None):
    query = str(query)
    simple = " "+string.lower(re.sub('[^ a-zA-Z0-9]','',query))+" "
    reply=""
    for k in Eliza.brain.keys():
      found = simple.find(' '+k+' ')
      if found > -1:
        if k == "":
          continue
        predicate = simple[found+len(k)+2:-1]
        if type(Eliza.brain[k]) == type(" "):
          k = Eliza.brain[k]
        reply = random.choice(Eliza.brain[k])
        reply = reply.replace('*',' '+predicate+'?')
    if reply == "":
      reply = random.choice(Eliza.brain[""])
    return reply


if __name__ == "__main__":
  eliza = Eliza()
  print "this is where Eliza would do some stuff, maybe an interactive shell."
  teststatements = [
     "I feel more like a woman."
    ,"I wish they wouldn't stare at me."
    ,"I can't deal with crowds."
    ,"Why do snakes give milk?"
    ]
  random.shuffle(teststatements)
  for s in teststatements:
    print "> %s" % s
    print eliza.input(s)
  print "... text complete."

