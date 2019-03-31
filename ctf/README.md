# Sunshine CTF

## Challenge #1: Patches Punches (reversing)


## Challenge #2: Wrestler Name Generator (web)

This challenge presented a website which, upon entering the first and last name and choosing a weapon of choice, would generate a wrestler name. The landing page looks like this:

![alt text](https://raw.githubusercontent.com/theo-kim/offensive-security/master/ctf/images/main.png)

```javascript
document.getElementById("button").onclick = function() {
  var firstName = document.getElementById("firstName").value;
  var lastName = document.getElementById("lastName").value;
  var input = btoa("<?xml version='1.0' encoding='UTF-8'?><input><firstName>" + firstName + "</firstName><lastName>" + lastName+ "</lastName></input>");
  window.location.href = "/generate.php?input="+encodeURIComponent(input);
};
```
