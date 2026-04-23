package stringutils;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class StringUtilsTest_v1 {
 
 @Test
 void testLeftPad() {
 assertEquals(" abc", StringUtils.leftPad("abc", 7));
 assertEquals("abc", StringUtils.leftPad("abc", 3));
 assertEquals("abc", StringUtils.leftPad("abc", 2));
 }
 
 @Test
 void testSplitByLines() {
 assertArrayEquals(new String[]{"ab","c"},StringUtils.splitByLines("[45D[K
String[]{"ab","c"},StringUtils.splitByLines("ab\nc"));
 assertArrayEquals(new String[]{""},StringUtils.splitByLines("\n"));[45D[K
String[]{""},StringUtils.splitByLines("\n"));
 }
 
 @Test
 void testSplitByChar() {
 assertArrayEquals(new String[]{"a","b","c"},StringUtils.splitBy("ab[45D[K
String[]{"a","b","c"},StringUtils.splitBy("abc", 'c'));
 assertArrayEquals(new String[]{""},StringUtils.splitBy("abcd", 'e')[4D[K
'e'));
 }
 
 @Test
 void testExtractInts() {
 assertArrayEquals(new int[]{1,2,3},StringUtils.extractInts("1 2 3")[3D[K
3"));
 }
 
 @Test
 void testEscapeForXML() {
 assertEquals("&lt;&gt;&amp;'\"", StringUtils.escapeForXML("<>&\"'\"[34D[K
StringUtils.escapeForXML("<>&\"'\""));
 }
 
 @Test
 void testSubstitute() {
 assertEquals("abcde", StringUtils.substitute("abcdaaabbbccc","aaa",[45D[K
StringUtils.substitute("abcdaaabbbccc","aaa","d"));
 assertEquals("abcdaaabbbccc", StringUtils.substitute("abcdaaabbbccc[37D[K
StringUtils.substitute("abcdaaabbbccc","zzz","d"));
 }
}