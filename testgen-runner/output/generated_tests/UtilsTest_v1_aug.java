package utils;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class UtilsTest {
 @Test
 void absoluteURLTest() {
 String url = "https://www.example.com";
 assertTrue(Utils.absoluteURL(url)); // URL should start with a protocol like "http://", "ftp://" or "https://"
 }
 
 @Test
 void absoluteURLAbsentTest() {
 String url = "example.com";
 assertFalse(Utils.absoluteURL(url)); // URL is relative without a protocol, should return false
 }

 @Test
 void encodePathAsIdentifierTest() {
 String path = "http://example.com";
 assertNotEquals("http_2F__example.com", Utils.encodePathAsIdentifier(path)); // Utils.encodePathAsIdentifier should return a valid Java identifier, not an URL encoded string
 }
 
 @Test
 void encodePathInvalidInputTest() {
 String path = "<script>alert('xss')</script>";
 assertThrows(Exception.class, () -> Utils.encodePath(path)); // Encoding a potentially harmful string should throw an exception
 }
 
 @Test
 void encodePathSpecialCharactersTest() {
 String path = "-_$~/\\*?";
 assertEquals("--__$$~~-_-", Utils.encodePath(path)); // The encoding function should escape all special characters
 }

 @Test
 void nCharsTest() {
 int n = 5;
 char c = 'a';
 assertEquals("aaaaa", Utils.nChars(n, c)); // The method should return a string of length 'n' filled with character 'c'
 }
 
 @Test
 void nCharsInvalidInputTest() {
 int n = 0;
 char c = 'a';
 assertThrows(IllegalArgumentException.class, () -> Utils.nChars(n, c)); // The method should throw IllegalArgumentException if the input is invalid (n <= 0)
 }

 @Test
 void pseudoAbsoluteURLTest() {
 String url = "/home/user";
 assertTrue(Utils.pseudoAbsoluteURL(url)); // A URL starting with a slash should return true
 }
 
 @Test
 void pseudoAbsoluteURLAbsentTest() {
 String url = "home/user";
 assertFalse(Utils.pseudoAbsoluteURL(url)); // A relative URL without the leading slash should return false
 }
}