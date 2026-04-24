package corina.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class StringUtilsTest_v1 {
 @Test
 void testLeftPad() {
 assertEquals(" hello", StringUtils.leftPad("hello", 8));
 assertEquals("hello", StringUtils.leftPad("hello", 5));
 }
 
 @Test
 void testSplitByLines() {
 assertArrayEquals(new String[] {"hello", "world"}, StringUtils.spli[16D[K
StringUtils.splitByLines("hello\nworld"));
 }
 
 @Test
 void testSplitByChar() {
 assertArrayEquals(new String[] {"he", "llo", "wo", "rld"}, StringUt[8D[K
StringUtils.splitBy('l', "hello world"));
 }
 
 @Test
 void testExtractInts() {
 assertArrayEquals(new int[] {1, 2, 3}, StringUtils.extractInts("1 2[1D[K
2 3"));
 }
 
 @Test
 void testEscapeForXML() {
 assertEquals("hello&amp;world", StringUtils.escapeForXML("hello&wor[35D[K
StringUtils.escapeForXML("hello&world"));
 }
 
 @Test
 void testSubstitute() {
 assertEquals("hey there world", StringUtils.substitute("hello there[5D[K
there world", "hello", "hey"));
 }
}