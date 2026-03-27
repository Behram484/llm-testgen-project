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
 void encodePathAsIdentifierTest() {
 String path = "http://example.com";
 assertFalse(Utils.encodePathAsIdentifier(path).equals("http_2F__example.com")); // Utils.encodePathAsIdentifier should return a valid Java identifier, not an URL encoded string
 }
 
 @Test
 void encodePathTest() {
 String path = "/home/user";
 assertEquals("-home-user", Utils.encodePath(path));
 }
 
 @Test
 void nCharsTest() {
 int n = 5;
 char c = 'a';
 assertEquals("aaaaa", Utils.nChars(n, c));
 }
 
 @Test
 void pseudoAbsoluteURLTest() {
 String url = "/home/user";
 assertTrue(Utils.pseudoAbsoluteURL(url));
 }
}