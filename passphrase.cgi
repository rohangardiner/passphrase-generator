#!/usr/bin/python

import cgi, os, sys, string, random, Cookie

sys.stderr = sys.stdout
debug = 1

def digit_gen(size, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def punctuation_gen(size=1, chars=string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))
def getword():
	return random.choice(open('common').read().split()).strip()
def formField(type,name,value,on):
	if on==1:
		print '<input type="'+type+'" name="'+name+'" value="'+value+'" CHECKED> '+name+'</input>'
	else:
		print '<input type="'+type+'" name="'+name+'" value="'+value+'"> '+name+'</input>'
		
# Calculate how many passwords generated and print on screen
def counter():
	fh = open ("count","r")
	hits=int(fh.read())+1
	fh.close()
	print "Unique passphrases created:",hits
	fw = open ("count","w")
	fw.write(str(hits))
	fw.close()

# Grab a random word from dictionary file 'common'
def getword():
	return random.choice(open('common').read().split()).strip()

def getRandomCap():
    passphraseList = list(passphrase)
    randomCapital = random.choice(passphraseList)
    while not randomCapital in alphabetList:
        randomCapital = random.choice(passphraseList)
        passphrase = passphrase.replace(randomCapital, randomCapital.capitalize())
	
# Set limits for number of words
minWordNum = 2
maxWordNum = 12

# Set up names for title
namesList = ['Peter', 'Karin', 'Chris', 'Danny', 'Jeff', 'Tom', 'Tori', 'Paul', 'Dan', 'Rohan', 'Karen']
randomName = random.choice(namesList)

# Set up colour theme for generator. This will be the Hue, we'll pick the Sat/Lum later
themeColourBase = str(random.randint(1,359))

# Set up list of random synbols if the user wants one
symbolList = ['!','@','#','$','%','^','&','*','+','=','?']
randomSymbol = random.choice(symbolList)
randomChoice = '<input type="Radio" name="delimiter" id="randsym" value="' +randomSymbol+ '" CHECKED> Random</input>'

# Set up alphabet for random capitals
alphabetList = list(string.ascii_letters)
# randomCapital = random.choice(alphabetList)

# Set up data variable to hold user responses
data = cgi.FieldStorage()

# Set up web page and styles
pageHeader = """Content-type: text/html\n
<head>
<title>HealthIT passphrase generator</title>\n
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab&display=swap" rel="stylesheet">
<link rel="icon" type="image/png" href="https://healthit.com.au/wp-content/uploads/2019/03/hit-logo-vector-whitebg.png"/>
<link rel="stylesheet" href="https://healthit.com.au/src/fontawesome/css/fontawesome.min.css">

<script type="text/javascript">
function copyPwd() {
    var copyString = document.getElementsByClassName('passphrase-output')[0].textContent;
    var copyTrim = copyString.slice(1,-1)
    navigator.clipboard.writeText(copyTrim)
    .then(() => {
        console.log('Text copied to clipboard');
        document.getElementsByClassName('confirmation')[0].style.visibility='visible';
        fadeOut(50)
        })
    .catch(err => {
        // This can happen if the user denies clipboard permissions:
        console.error('Could not copy text: ', err);
      });
  }

function similarPwd(similar) {
    console.log('Similar password clicked');
    window.location.reload();
    // document.getElementsByClassName('passphrase-output')[0].innerText = similar;
}
  
function fadeOut(speed) {
    var s = document.getElementsByClassName('confirmation')[0].style;
    s.opacity = 4;
    (function fade() {(s.opacity-=.1)<.1?s.visibility="hide":setTimeout(fade,speed)})();
}
</script>

<style>
body {
    background-color: #d6fffd;
    font-family: 'Open Sans', sans-serif;
}

h1 {
    display: inline;
}

table {
    border-collapse: collapse;
}

#content table {
  text-align: left;
  border: 1px solid #dbdbdb;
  border-collapse: collapse;
}

#wrapper {
  text-align: center;
}

#title {
  background-image: linear-gradient(-90deg, #00b5e2, #0a2f4c);
  padding: 1px 10px;
  text-align: center;
  width: 100%;
  margin: -10px -10px 10px -10px;
  color: white;
}

.title-logo {
    z-index: 9;
    position: absolute;
    top: 0;
    left: 10;
    background: #f0fffe;
    padding: 8px 0;
    -webkit-box-shadow: 0px 3px 5px 1px rgba(94,94,94,0.5);
    -moz-box-shadow: 0px 3px 5px 1px rgba(94,94,94,0.5);
    box-shadow: 0px 3px 5px 1px rgba(94,94,94,0.5);
}

.title-logo img {
    max-height: 60px;
}

#content {
  text-align: center;
  border-radius: 2px;
  border-color: #dbdbdb;
  /*background-image: linear-gradient(-90deg, #ffd188, #ffd788);*/
  background-color: #f7feff;
  padding: 10px;
  margin: 15px auto;
  width: 75%;
  -webkit-box-shadow: 0px 4px 11px 1px rgba(150,148,150,1);
  -moz-box-shadow: 0px 4px 11px 1px rgba(150,148,150,1);
  box-shadow: 0px 4px 11px 1px rgba(150,148,150,1);
  /*box-shadow: 6px 6px 8px #c4c4c4;*/
}

.passphrase-output {
    font-family: 'Roboto Slab', serif;
    color: blue;
}

#logo-footer {
  /*position: fixed;
  bottom: 0;*/
  padding: 25px;
}

.nice-btn {
padding: 10px 15px;
margin: 0 10px;
color: #fff;
font-weight: bold;
font-size: 11pt;
/*background-color handled inline, I'll fix later*/
border: 0 solid #fff;
border-radius: 4px;
-webkit-box-shadow: 0px 4px 6px -2px rgba(151,148,150,0.75);
-moz-box-shadow: 0px 4px 6px -2px rgba(151,148,150,0.75);
box-shadow: 0px 4px 6px -2px rgba(151,148,150,0.75);
cursor: pointer;
}

#presets form, output-actions {
    display: inline;
}

.confirmation {
    color: blue;
    font-weight: bold;
    padding-left: 20px;
    visibility: hidden;
}
</style>
</head>
"""

# Create form elements
formStart = '<P><form method="POST" action="">'
formEnd = '<input type="Submit" value="Generate Passphrase" class="nice-btn" style="background-color: hsl('+themeColourBase+', 50%, 60%)"></form>'

# Start displaying the web page
print pageHeader
print '<body style="background-color: hsl('+themeColourBase+', 50%, 90%)">'

print '<div id="wrapper">'
print '<div id="title" style="background-image: linear-gradient(-90deg, hsl('+themeColourBase+', 50%, 60%), hsl('+themeColourBase+', 50%, 30%));"><h2>'+randomName+'\'s better passphrase generator</h2></div>'
print '<div id="logo-image-title" class="title-logo"><a href="https://healthit.com.au"><img src="https://healthit.com.au/wp-content/uploads/2019/06/HIT-proper-logo.png"></a></div>'
print '<div id="content">'

# Print preset buttons
print '<div id = "presets">'

# Short
print '<form method="post" action"">'
print '<input type="hidden" name="wordnum" value="2">'
print '<input type="hidden" name="delimiter" value="' +randomSymbol+ '">'
print '<input type="hidden" name="caps" value="1" CHECKED>'
print '<input type="hidden" name="randnum" value="1" CHECKED>'
print '<input type="submit" value="Short passphrase" class="nice-btn" style="background-color: hsl('+themeColourBase+', 50%, 60%)">'
print '</form>'

# Medium
print '<form method="post" action"">'
print '<input type="hidden" name="wordnum" value="'+str(random.randint(3,4))+'">'
print '<input type="hidden" name="delimiter" value="'+randomSymbol+'">'
print '<input type="hidden" name="caps" value="'+str(random.randint(0,1))+'">'
print '<input type="hidden" name="randnum" value="'+str(random.randint(0,1))+'">'
print '<input type="submit" value="Medium passphrase" class="nice-btn" style="background-color: hsl('+themeColourBase+', 50%, 60%)">'
print '</form>'

# Long
print '<form method="post" action"">'
print '<input type="hidden" name="wordnum" value="'+str(random.randint(4,5))+'">'
print '<input type="hidden" name="delimiter" value="' +randomSymbol+ '">'
print '<input type="hidden" name="caps" value="'+str(random.randint(0,1))+'">'
print '<input type="hidden" name="randnum" value="1" CHECKED>'
print '<input type="hidden" name="randcaps" value="No">'
print '<input type="submit" value="Long passphrase" class="nice-btn" style="background-color: hsl('+themeColourBase+', 50%, 60%)">'
print '</form></div>'

print formStart
print '<TABLE BORDER=1 cellpadding="10" WIDTH="100%"><tr><td>'

# Number of words selection. Suggest you default this to no less than 4.
if 'wordnum' in data:
	wordnum=data['wordnum'].value
	print '<H3><input type="number" name="wordnum" value="'+wordnum+'" min="2" max="12"> Number of words </H3>'
else:
	# we don't have a value so will draw with default value
	print '<H3><input type="number" name="wordnum" value="4" min="2" max="12"> Number of words </H3>'
	wordnum=4

# Delimiter

print '<H3>Separator:</H3>'

# Print out our range of radio button options
# This should be the right way to do it but it's getting weird.
# for i in ['dot','comma','dash','none','random']:
#	if data.has_key(i):
#		print formField("radio",i,i,"1")
#		delim=i
#	else:
#		print formField("radio",i,i,"0")
#		delim='blank'

# Default fallback
try:
 delim = data['delimiter'].value
except:
 delim = "_"

if delim == ".":
	print '<input type="Radio" name="delimiter" id="dot" value="." CHECKED> Dot</input>'
else:
	print '<input type="Radio" name="delimiter" id="dot" value="."> Dot</input>'
if delim == ",":
	print '<input type="Radio" name="delimiter" id="comma" value="," CHECKED> Comma</input>'
else:
	print '<input type="Radio" name="delimiter" id="comma" value=","> Comma</input>'
if delim == "-":
	print '<input type="Radio" name="delimiter" id="dash" value="-" CHECKED> Dash</input>'
else:
	print '<input type="Radio" name="delimiter" id="dash" value="-"> Dash</input>'
if delim =="_":
	delim="_"
	print '<input type="Radio" name="delimiter" id="blank" value="_" CHECKED> Blank</input>'
else:
	print '<input type="Radio" name="delimiter" id="blank" value="_"> Blank</input>'
if delim in symbolList:
    print '<input type="Radio" name="delimiter" id="randsym" value="' +randomSymbol+ '" CHECKED> Random</input>'
else:
    print '<input type="Radio" name="delimiter" id="randsym" value="' +randomSymbol+ '"> Random</input>'

print "<p>"

if 'caps' in data:
        print '<H3><input type="Checkbox" name="caps" value="1" CHECKED> Capitalise words</input></H3>'
else:
        print '<H3><input type="Checkbox" name="caps" value="1"> Capitalise words</input></H3>'
print '<p>'
if 'randcaps' in data:
        print '<H3><input type="Checkbox" name="randcaps" value="1" CHECKED> Random capitals</input></H3>'
else:
        print '<H3><input type="Checkbox" name="randcaps" value="1"> Random capitals</input></H3>'
print '<p>'
if 'randnum' in data:
        print '<H3><input type="Checkbox" name="randnum" value="1" CHECKED> Append Random Number</input></H3>'
else:
        print '<H3><input type="Checkbox" name="randnum"> Append Random Number</input></H3>'

print '<BR><BR>'
print formEnd
print '</TD><TD>'

passphrase=""

# Create list of words and delimiters for passphrase
newPassphraseAsList = []
if data:
    while wordnum:
        word = str(getword())
        if 'caps'in data:
            word = str.capitalize(word)
        newPassphraseAsList.append(word)
        newPassphraseAsList.append(delim)
        wordnum = int(wordnum)-1

# Trim extraneous delimiter
if data:
    del newPassphraseAsList[-1]

# Add a random number if the user wants
if 'randnum' in data:
    newPassphraseAsList.append(str(random.randint(1,999)))

# Assemble the passphrase from list parts
passphrase = ''.join(newPassphraseAsList)

# Get a list of the first letters of each word in passphrase for similar button
lettersList = [i[0] for i in newPassphraseAsList]

#Roll a similar password if the user wants
if data:
    similarPassphraseAsList = []

for i in lettersList:
    if i in alphabetList:
        # It's a letter
        bookFile = open('common', 'r')
        sameLetterList = [x for x in bookFile.read().lower().split() if x.startswith((i).lower())]
        if 'caps' in data:
            similarPassphraseAsList.append(str.capitalize(random.choice(sameLetterList)))
        else:
            similarPassphraseAsList.append(random.choice(sameLetterList))
    elif i in symbolList:
        # It's a delimiter
        similarPassphraseAsList.append(i)
    else:
        #It's a number or unknown
        similarPassphraseAsList.append(newPassphraseAsList[-1])

if data:
    similarPassphrase = ''.join(similarPassphraseAsList)

# Ok so in the next bit the final character gets stripped before adding a random
# number and I couldn't get a conditional to work so I ended up just adding a
# sacrificial character to get stripped so that the whole word would show.
# Don't make fun of me I've been stuck on this for an hour
if delim == "_":
 passphrase = passphrase+"."

# Check if using random capitals, get a list of characters in the passphrase
# Check that list against a list of acceptable letters and capitalise the chosen
if 'randcaps' in data:
    passphraseList = list(passphrase)
    randomCapital = random.choice(passphraseList)
    while not randomCapital in alphabetList:
        randomCapital = random.choice(passphraseList)
    passphrase = passphrase.replace(randomCapital, randomCapital.capitalize())
    
# If passphrase variable isn't empty, print passphrase. Else print a welcome message
if not passphrase == ".":
    print '<H3>Your Unique Passphrase:<BR></H3><HR><H1><span class="passphrase-output">', passphrase.replace("_", ""),'</span></H1><br>'
    print '<span class="copy-btn" onclick="copyPwd();">Copy</span><span class="similar-btn" onclick="similarPwd(\'%s\');">Similar</span><HR><BR>' % similarPassphrase
    counter()
    print '<span class="confirmation">Copied to clipboard!</span>'
else:
    print '<H3>Use the options on the left<BR></H3><HR><H2><span class="passphrase-output">Create your unique passphrase</span></H2><HR><BR>'
    print 'More secure than just a password, and easier to remember'

print '</TD></TR></TABLE><BR>'
print "</UL>"

# Close content and display footer
print '''
</div>
<div id="logo-footer">
<a href="https://healthit.com.au">
<img src="https://healthit.com.au/wp-content/uploads/2019/06/HIT-proper-logo.png" width="25% height="25%">
</a>
</div>
</div>
'''

# These lines are for debugging, please omit from live page
print data
print '<br>Keys:'
print data.keys()
print '<br> Delimiter value:'
print data['delimiter'].value
print '<br>Random:'
print randomSymbol
print '<br>PassphraseAsList:'
print newPassphraseAsList
print '<br>letters list:'
print lettersList
print '<br> Similar passphrase:'
print similarPassphraseAsList
print '<br>Similar passphrase as string:'
print similarPassphrase
print '<br> Random capital:'
try:
    print randomCapital
except:
    print 'N/A'
print '<br>To do: captcha/grab random word from internet, user confirms real word, add to dictionary, minimum 10 characters short pwd, maximum 15-16 short password'

print "</body></html>"
