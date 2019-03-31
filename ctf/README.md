# Sunshine CTF

## Challenge #1: Patches Punches (reversing)


## Challenge #2: Wrestler Name Generator (web)

This challenge presented a website which, upon entering the first and last name and choosing a weapon of choice, would generate a wrestler name. The landing page looks like this:

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

Immediately, I thought about exploiting the common XXE (XML External Entity) vulnerability. Rather than entering the XML exploit into the input element of the website, I tried passing the XML string drectly into the URL `http://ng.sunshinectf.org/generate.php?input=[XML]`.
