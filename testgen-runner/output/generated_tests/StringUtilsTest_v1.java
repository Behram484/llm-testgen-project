package stringutils;

import static org.junit.jupiter.api.Assertions.*;

class StringUtilsTest_v1 {
 
 // Testing leftPad method
 @org.junit.jupiter.api.Test
 void testLeftPad() {
 assertEquals(" hello", StringUtils.leftPad("hello", 8));
 assertThrows(IllegalArgumentException.class, () -> StringUtils.leftPad(null, 5));
 assertEquals("world", StringUtils.leftPad("world", 5));
 }
 
 // Testing splitByLines method
 @org.junit.jupiter.api.Test
 void testSplitByLines() {
 assertArrayEquals(new String[]{"a","b","c"}, StringUtils.splitByLines("a\nb\nc"));
 }
 
 // Testing splitBy method
 @org.junit.jupiterapi.Test
 void testSplitBy() {
 assertArrayEquals(new String[]{"abc","def","ghi"}, StringUtils.splitBy("\n", 'a', "bc\ndef\nghi"));
 }
 
 // Testing extractInts method
 @org.junit.jupiter.api.Test
 void testExtractInts() {
 assertArrayEquals(new int[]{1, 2, 3}, StringUtils.extractInts("1 2 3"));
 }
 
 // Testing escapeForXML method
 @org.junit.jupiter.api.Test
 void testEscapeForXML() {
 assertEquals("&amp;lt;dating&amp;gt;&amp;#x0D;&amp;lt;/dating&amp;gt;", StringUtils.escapeForXML("<dating>\r</dating>"));
 }
 
 // Testing substitute method
 @org.junit.jupiter.api.Test
 void testSubstitute() {
 assertEquals("hello there", StringUtils.substitute("hello world", "world", "there"));
 }
}