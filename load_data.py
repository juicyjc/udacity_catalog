#
# load_data.py - populate DB with sample data for the Catalog App
#

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Users
user1 = User(name='Jeremy Collins', email='collins.jeremy@gmail.com',
             picture='https://lh6.googleusercontent.com/-GXBUIlrTwRc/AAAAAAAAAAI/AAAAAAAAAzw/sMLp3XJE5qg/photo.jpg')
session.add(user1)
session.commit()

jc = session.query(User).filter_by(email='collins.jeremy@gmail.com').one()

# Genres
category1 = Category(name='Science Fiction', user_id=jc.id)
session.add(category1)
session.commit()

category2 = Category(name='Young Adult', user_id=jc.id)
session.add(category2)
session.commit()

category3 = Category(name='Memoir', user_id=jc.id)
session.add(category3)
session.commit()

category4 = Category(name='Romance', user_id=jc.id)
session.add(category4)
session.commit()

category5 = Category(name='Fantasy', user_id=jc.id)
session.add(category5)
session.commit()

category6 = Category(name='Crime Thriller', user_id=jc.id)
session.add(category6)
session.commit()

category7 = Category(name='Computers', user_id=jc.id)
session.add(category7)
session.commit()

category8 = Category(name='Comics', user_id=jc.id)
session.add(category8)
session.commit()

category9 = Category(name='Children', user_id=jc.id)
session.add(category9)
session.commit()

# Items
# Science Fiction
category = session.query(Category).filter_by(name='Science Fiction').one()

item = Item(category_id=category.id,
            name='Lord of Light',
            description="In the 1960s, Roger Zelazny dazzled the SF world with what seemed to be inexhaustible talent and inventiveness. Lord of Light, his third novel, is his finest book: a science fantasy in which the intricate, colorful mechanisms of Hindu religion, capricious gods, and repeated reincarnations are wittily underpinned by technology. \"For six days he had offered many kilowatts of prayer, but the static kept him from being heard On High.\" The gods are a starship crew who subdued a colony world; developed godlike--though often machine-enhanced--powers during successive lifetimes of mind transfer to new, cloned bodies; and now lord it over descendants of the ship's mere passengers. Their tyranny is opposed by retired god Sam, who mocks the Celestial City, introduces Buddhism to subvert Hindu dogma, allies himself with the planet's native \"demons\" against Heaven, fights pyrotechnic battles with bizarre troops and weapons, plays dirty with politics and poison, and dies horribly but won't stay dead. It's a huge, lumbering, magical story, told largely in flashback, full of wonderfully ornate language (and one unforgivable pun) that builds up the luminous myth of trickster Sam, Lord of Light. Essential SF reading.",
            image_name='lord_of_light.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Shadow and Claw',
            description="The Book of the New Sun is unanimously acclaimed as Gene Wolfe's most remarkable work, hailed as \"a masterpiece of science fantasy comparable in importance to the major works of Tolkien and Lewis\" by Publishers Weekly, and \"one of the most ambitious works of speculative fiction in the twentieth century\" by The Magazine of Fantasy and Science Fiction. Shadow & Claw brings together the first two books of the tetralogy in one volume: The Shadow of the Torturer is the tale of young Severian, an apprentice in the Guild of Torturers on the world called Urth, exiled for committing the ultimate sin of his profession -- showing mercy toward his victim. The Claw of the Conciliator continues the saga of Severian, banished from his home, as he undertakes a mythic quest to discover the awesome power of an ancient relic, and learn the truth about his hidden destiny.",
            image_name='shadow_and_claw.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Sword and Citadel',
            description="The Book of the New Sun is unanimously acclaimed as Gene Wolfe's most remarkable work, hailed as \"a masterpiece of science fantasy comparable in importance to the major works of Tolkien and Lewis\" by Publishers Weekly, and \"one of the most ambitious works of speculative fiction in the twentieth century\" by The Magazine of Fantasy and Science Fiction. Sword & Citadel brings together the final two books of the tetralogy in one volume: The Sword of the Lictor is the third volume in Wolfe's remarkable epic, chronicling the odyssey of the wandering pilgrim called Severian, driven by a powerful and unfathomable destiny, as he carries out a dark mission far from his home. The Citadel of the Autarch brings The Book of the New Sun to its harrowing conclusion, as Severian clashes in a final reckoning with the dread Autarch, fulfilling an ancient prophecy that will forever alter the realm known as Urth.",
            image_name='sword_and_citadel.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Young Adult
category = session.query(Category).filter_by(name='Young Adult').one()

item = Item(category_id=category.id,
            name="Harry Potter And The Sorcerer's Stone",
            description="Harry Potter has no idea how famous he is. That's because he's being raised by his miserable aunt and uncle who are terrified Harry will learn that he's really a wizard, just as his parents were. But everything changes when Harry is summoned to attend an infamous school for wizards, and he begins to discover some clues about his illustrious birthright. From the surprising way he is greeted by a lovable giant, to the unique curriculum and colorful faculty at his unusual school, Harry finds himself drawn deep inside a mystical world he never knew existed and closer to his own noble destiny.",
            image_name='hp_sorcerers_stone.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Chamber Of Secrets',
            description="The Dursleys were so mean that hideous summer that all Harry Potter wanted was to get back to the Hogwarts School for Witchcraft and Wizardry. But just as he's packing his bags, Harry receives a warning from a strange, impish creature named Dobby who says that if Harry Potter returns to Hogwarts, disaster will strike. And strike it does. For in Harry's second year at Hogwarts, fresh torments and horrors arise, including an outrageously stuck-up new professor, Gilderoy Lockheart, a spirit named Moaning Myrtle who haunts the girls' bathroom, and the unwanted attentions of Ron Weasley's younger sister, Ginny. But each of these seem minor annoyances when the real trouble begins, and someone--or something--starts turning Hogwarts students to stone. Could it be Draco Malfoy, a more poisonous rival than ever? Could it possibly be Hagrid, whose mysterious past is finally told? Or could it be the one everyone at Hogwarts most suspects...Harry Potter himself?",
            image_name='hp_chamber_of_secrets.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Prisoner of Azkaban',
            description="For twelve long years, the dread fortress of Azkaban held an infamous prisoner named Sirius Black. Convicted of killing thirteen people with a single curse, he was said to be the heir apparent to the Dark Lord, Voldemort. Now he has escaped, leaving only two clues as to where he might be headed: Harry Potter's defeat of You-Know-Who was Black's downfall as well. And the Azkban guards heard Black muttering in his sleep, \"He's at Hogwarts...he's at Hogwarts.\" Harry Potter isn't safe, not even within the walls of his magical school, surrounded by his friends. Because on top of it all, there may well be a traitor in their midst.",
            image_name='hp_Prisoner_of_Azkaban.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Order Of The Phoenix',
            description="As his fifth year at Hogwarts School of Witchcraft and Wizardry approaches, 15-year-old Harry Potter is in full-blown adolescence, complete with regular outbursts of rage, a nearly debilitating crush, and the blooming of a powerful sense of rebellion. It's been yet another infuriating and boring summer with the despicable Dursleys, this time with minimal contact from our hero's non-Muggle friends from school. Harry is feeling especially edgy at the lack of news from the magic world, wondering when the freshly revived evil Lord Voldemort will strike. Returning to Hogwarts will be a relief... or will it?",
            image_name='hp_Order_of_the_Phoenix.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Half-Blood Prince',
            description="The war against Voldemort is not going well; even the Muggles have been affected. Dumbledore is absent from Hogwarts for long stretches of time, and the Order of the Phoenix has already suffered losses. And yet . . . as with all wars, life goes on. Sixth-year students learn to Apparate. Teenagers flirt and fight and fall in love. Harry receives some extraordinary help in Potions from the mysterious Half-Blood Prince. And with Dumbledore's guidance, he seeks out the full, complex story of the boy who became Lord Voldemort -- and thus finds what may be his only vulnerability.",
            image_name='hp_Half-Blood_Prince.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Goblet Of Fire',
            description="The paperback edition of the legendary, record-breaking, best-selling fourth Harry Potter novel. Harry Potter is midway through his training as a wizard and his coming of age. Harry wants to get away from the pernicious Dursleys and go to the International Quidditch Cup. He wants to find out about the mysterious event that's supposed to take place at Hogwarts this year, an event involving two other rival schools of magic, and a competition that hasn't happened for a hundred years. He wants to be a normal, fourteen-year-old wizard. But unfortunately for Harry Potter, he's not normal - even by wizarding standards. And in his case, different can be deadly.",
            image_name='hp_Goblet_of_Fire.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Harry Potter And The Deathly Hallows',
            description="Readers beware. The brilliant, breathtaking conclusion to J.K. Rowling's spellbinding series is not for the faint of heart--such revelations, battles, and betrayals await in Harry Potter and the Deathly Hallows that no fan will make it to the end unscathed. Luckily, Rowling has prepped loyal readers for the end of her series by doling out increasingly dark and dangerous tales of magic and mystery, shot through with lessons about honor and contempt, love and loss, and right and wrong. Fear not, you will find no spoilers in our review--to tell the plot would ruin the journey, and Harry Potter and the Deathly Hallows is an odyssey the likes of which Rowling's fans have not yet seen, and are not likely to forget. But we would be remiss if we did not offer one small suggestion before you embark on your final adventure with Harry--bring plenty of tissues. The heart of Book 7 is a hero's mission--not just in Harry's quest for the Horcruxes, but in his journey from boy to man--and Harry faces more danger than that found in all six books combined, from the direct threat of the Death Eaters and you-know-who, to the subtle perils of losing faith in himself. Attentive readers would do well to remember Dumbledore's warning about making the choice between \"what is right and what is easy,\" and know that Rowling applies the same difficult principle to the conclusion of her series. While fans will find the answers to hotly speculated questions about Dumbledore, Snape, and you-know-who, it is a testament to Rowling's skill as a storyteller that even the most astute and careful reader will be taken by surprise. A spectacular finish to a phenomenal series, Harry Potter and the Deathly Hallows is a bittersweet read for fans. The journey is hard, filled with events both tragic and triumphant, the battlefield littered with the bodies of the dearest and despised, but the final chapter is as brilliant and blinding as a phoenix's flame, and fans and skeptics alike will emerge from the confines of the story with full but heavy hearts, giddy and grateful for the experience.",
            image_name='hp_Deathly_Hallows.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Memoir
category = session.query(Category).filter_by(name='Memoir').one()

item = Item(category_id=category.id,
            name='Ghost Boy',
            description="They all thought he was gone. But he was alive and trapped inside his own body for ten years. In January 1988 Martin Pistorius, age twelve, fell inexplicably sick. First he lost his voice and stopped eating. Then he slept constantly and shunned human contact. Doctors were mystified. Within eighteen months he was mute and wheelchair bound. Martin's parents were told an unknown degenerative disease left him with the mind of a baby and less than two years to live. Martin was moved to care centers for severely disabled children. The stress and heartache shook his parents' marriage and their family to the core. Their boy was gone. Or so they thought. Ghost Boy is the heart-wrenching story of one boy's return to life through the power of love and faith. In these pages, readers see a parent's resilience, the consequences of misdiagnosis, abuse at the hands of cruel caretakers, and the unthinkable duration of Martin's mental alertness betrayed by his lifeless body. We also see a life reclaimed, a business created, a new love kindled - all from a wheelchair. Martin's emergence from his own darkness invites us to celebrate our own lives and fight for a better life for others.",
            image_name='ghost-boy_large.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Wild: From Lost to Found on the Pacific Crest Trail',
            description="At age 26, following the death of her mother, divorce, and a run of reckless behavior, Cheryl Strayed found herself alone near the foot of the Pacific Crest Trail--inexperienced, over-equipped, and desperate to reclaim her life. Wild tracks Strayed's personal journey on the PCT through California and Oregon, as she comes to terms with devastating loss and her unpredictable reactions to it. While readers looking for adventure or a naturalist's perspective may be distracted by the emotional odyssey at the core of the story, Wild vividly describes the grueling life of the long-distance hiker, the ubiquitous perils of the PCT, and its peculiar community of wanderers. Others may find her unsympathetic--just one victim of her own questionable choices. But Strayed doesn't want sympathy, and her confident prose stands on its own, deftly pulling both threads into a story that inhabits a unique riparian zone between wilderness tale and personal-redemption memoir.",
            image_name='wild.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Romance
category = session.query(Category).filter_by(name='Romance').one()

item = Item(category_id=category.id,
            name="The Time Traveler's Wife",
            description="The Time Traveler's Wife is the debut novel of American author Audrey Niffenegger, published in 2003. It is a love story about a man with a genetic disorder that causes him to time travel unpredictably, and about his wife, an artist, who has to cope with his frequent absences and dangerous experiences. Niffenegger, frustrated in love when she began the work, wrote the story as a metaphor for her failed relationships. The tale's central relationship came to her suddenly and subsequently supplied the novel's title. The novel, which has been classified as both science fiction and romance, examines issues of love, loss, and free will. In particular, it uses time travel to explore miscommunication and distance in relationships, while also investigating deeper existential questions.",
            image_name='time_travelers_wife.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Fantasy
category = session.query(Category).filter_by(name='Fantasy').one()

item = Item(category_id=category.id,
            name='Grass',
            description="Generations in the future, when humanity has spread to other planets and Earth is ruled by Sanctity, a dour, coercive religion that looks to resurrection of the body by storing cell samples of its communicants, a plague is threatening to wipe out mankind. The only planet that seems to be spared is Grass, so-called because that is virtually all that grows there. It was settled by families of European nobility who live on vast estancias and indulge in the ancient sport of fox hunting--although the horses, hounds and foxes aren't what they what they appear to be. Rigo and Marjorie Westriding Yrarier and family are sent to Grass as ambassadors and unofficial investigators because the ruling families--the bons--have refused to allow scientists to authenticate the planet's immunity from the plague. The egotistical Rigo sets out to prove himself to the bons while Marjorie remains wary about the relationship between the hunters and the hunted. She gains allies in her search, but invasion strikes from an unexpected quarter before the truth about an alien species comes to light. Tepper (The Gate to Women's Country) delves into the nature of truth and religion, creating some strong characters in her compelling story.",
            image_name='grass-sheri-tepper.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='The Eye of the World (The Wheel of Time, Book 1)',
            description="The Wheel of Time turns and Ages come and go, leaving memories that become legend. Legend fades to myth, and even myth is long forgotten when the Age that gave it birth returns again. In the Third Age, an Age of Prophecy, the World and Time themselves hang in the balance. What was, what will be, and what is, may yet fall under the Shadow. The peaceful villagers of Emond's Field pay little heed to rumors of war in the western lands until a savage attack by troll-like minions of the Dark One forces three young men to confront a destiny which has its origins in the time known as The Breaking of the World. This richly detailed fantasy presents a fully realized, complex adventure which will appeal to fans of classic quests.",
            image_name='TheEyeOfTheWorld.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Crime Thriller
category = session.query(Category).filter_by(name='Crime Thriller').one()

item = Item(category_id=category.id,
            name='The Bat',
            description="Inspector Harry Hole of the Oslo Crime Squad is dispatched to Sydney to observe a murder case. Harry is free to offer assistance, but he has firm instructions to stay out of trouble. The victim is a twenty-three year old Norwegian woman who is a minor celebrity back home. Never one to sit on the sidelines, Harry befriends one of the lead detectives, and one of the witnesses, as he is drawn deeper into the case. Together, they discover that this is only the latest in a string of unsolved murders, and the pattern points toward a psychopath working his way across the country. As they circle closer and closer to the killer, Harry begins to fear that no one is safe, least of all those investigating the case.",
            image_name='The-Bat-Jo-Nesbo.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='The Girl with the Dragon Tattoo',
            description="Once you start The Girl with the Dragon Tattoo, there's no turning back. This debut thriller--the first in a trilogy from the late Stieg Larsson--is a serious page-turner rivaling the best of Charlie Huston and Michael Connelly. Mikael Blomkvist, a once-respected financial journalist, watches his professional life rapidly crumble around him. Prospects appear bleak until an unexpected (and unsettling) offer to resurrect his name is extended by an old-school titan of Swedish industry. The catch--and there's always a catch--is that Blomkvist must first spend a year researching a mysterious disappearance that has remained unsolved for nearly four decades. With few other options, he accepts and enlists the help of investigator Lisbeth Salander, a misunderstood genius with a cache of authority issues. Little is as it seems in Larsson's novel, but there is at least one constant: you really don't want to mess with the girl with the dragon tattoo.",
            image_name='the_girl_with_the_dragon_tattoo.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Computers
category = session.query(Category).filter_by(name='Computers').one()

item = Item(category_id=category.id,
            name='Code: The Hidden Language of Computer Hardware and Software',
            description="Charles Petzold's latest book, Code: The Hidden Language of Computer Hardware and Software, crosses over into general-interest nonfiction from his usual programming genre. It's a carefully written, carefully researched gem that will appeal to anyone who wants to understand computer technology at its essence. Readers learn about number systems (decimal, octal, binary, and all that) through Petzold's patient (and frequently entertaining) prose and then discover the logical systems that are used to process them. There's loads of historical information too. From Louis Braille's development of his eponymous raised-dot code to Intel Corporation's release of its early microprocessors, Petzold presents stories of people trying to communicate with (and by means of) mechanical and electrical devices. It's a fascinating progression of technologies, and Petzold presents a clear statement of how they fit together. The real value of Code is in its explanation of technologies that have been obscured for years behind fancy user interfaces and programming environments, which, in the name of rapid application development, insulate the programmer from the machine. In a section on machine language, Petzold dissects the instruction sets of the genre-defining Intel 8080 and Motorola 6800 processors. He walks the reader through the process of performing various operations with each chip, explaining which opcodes poke which values into which registers along the way. Petzold knows that the hidden language of computers exhibits real beauty. In Code, he helps readers appreciate it.",
            image_name='code.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='Introducing Python: Modern Computing in Simple Packages',
            description="Easy to understand and fun to read, Introducing Python is ideal for beginning programmers as well as those new to the language. Author Bill Lubanovic takes you from the basics to more involved and varied topics, mixing tutorials with cookbook-style code recipes to explain concepts in Python 3. End-of-chapter exercises help you practice what you've learned. You'll gain a strong foundation in the language, including best practices for testing, debugging, code reuse, and other development tips. This book also shows you how to use Python for applications in business, science, and the arts, using various Python tools and open source packages. - Learn simple data types, and basic math and text operations - Use data-wrangling techniques with Python's built-in data structures - Explore Python code structure, including the use of functions - Write large programs in Python, with modules and packages - Dive into objects, classes, and other object-oriented features - Examine storage from flat files to relational databases and NoSQL - Use Python to build web clients, servers, APIs, and services - Manage system tasks such as programs, processes, and threads - Understand the basics of concurrency and network programming",
            image_name='introducing_python.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Comics
category = session.query(Category).filter_by(name='Comics').one()

item = Item(category_id=category.id,
            name='Milk and Cheese: Dairy Products Gone Bad',
            description="A carton of hate. A wedge of spite. A comic book of idiotic genius. The Eisner Award-winning dairy duo returns in this deluxe hardcover collecting every single stupid Milk and Cheese comic ever made from 1989 to 2010, along with a sh*t ton of supplemental awesomeness. This has everything you need! Don't judge it - love it! Or else!",
            image_name='Milk_and_Cheese.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='The Maxx: Maxximized Volume 1',
            description="Sam Kieth's own quirky brand of brilliance has been wowing fans and inspiring cartoonists for more than 25 years. As one of the earliest creators for Image Comics, Kieth created The Maxx - a homeless superhero who lives in a box. Both Maxx and his social worker friend, Julie, share adventures in both the real world and in \"the Outback,\" a fantasy realm inhabited by their jungle-inspired totems. In this new edition, each page has been scanned from the original art, remastered, and completely recolored under the watchful eye of Sam Kieth.",
            image_name='the_maxx.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

# Children
category = session.query(Category).filter_by(name='Children').one()

item = Item(category_id=category.id,
            name='The Stinky Cheese Man',
            description="If geese had graves, Mother Goose would be rolling in hers. The Stinky Cheese Man and Other Fairly Stupid Tales retells--and wreaks havoc on--the allegories we all thought we knew by heart. In these irreverent variations on well-known themes, the ugly duckling grows up to be an ugly duck, and the princess who kisses the frog wins only a mouthful of amphibian slime. The Stinky Cheese Man deconstructs not only the tradition of the fairy tale but also the entire notion of a book. Our naughty narrator, Jack, makes a mockery of the title page, the table of contents, and even the endpaper by shuffling, scoffing, and generally paying no mind to structure. Characters slide in and out of tales; Cinderella rebuffs Rumpelstiltskin, and the Giant at the top of the beanstalk snacks on the Little Red Hen. There are no lessons to be learned or morals to take to heart--just good, sarcastic fun that smart-alecks of all ages will love.",
            image_name='stinky.jpg',
            user_id=jc.id)
session.add(item)
session.commit()

item = Item(category_id=category.id,
            name='I Yam a Donkey!',
            description="Even frustrated grammarians will giggle at the who's-on-first routine that begins with a donkey's excited announcement, \"I yam a donkey!\" Unfortunately the donkey's audience happens to be a yam, and one who is particular about sloppy pronunciation and poor grammar. An escalating series of misunderstandings leaves the yam furious and the clueless donkey bewildered by the yam's growing (and amusing) frustration. The yam finally gets his point across, but regrettably, he's made the situation a little bit too clear . . . and the story ends with a dark and outrageously funny twist.",
            image_name='i_yam_donkey.jpg',
            user_id=jc.id)
session.add(item)
session.commit()
