package util;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class UtilTest_v1 {

 @Test
 void testStringIsEmpty() {
 assertTrue(Util.StringIsEmpty(""));
 assertFalse(Util.StringIsEmpty(" "));
 assertTrue(Util.StringIsEmpty(null));
 }

 @Test
 void testNormalizeString() {
 assertEquals("", Util.NormalizeString(null));
 assertEquals("test", Util.NormalizeString("test"));
 }

 @Test
 void testStringCompare() {
 assertEquals(0, Util.StringCompare("test", "test"));
 assertTrue(Util.StringCompare("test1", "test2") < 0);
 assertTrue(Util.StringCompare("test2", "test1") > 0);
 }

 @Test
 void testStringCompareIgnCase() {
 assertEquals(0, Util.StringCompareIgnCase("test", "TEST"));
 assertTrue(Util.StringCompareIgnCase("test1", "test2") < 0);
 assertTrue(Util.StringCompareIgnCase("test2", "test1") > 0);
 }

 @Test
 void testIntMaxString() {
 assertEquals("", Util.IntMaxString(Integer.MAX_VALUE));
 assertEquals("1234567890", Util.IntMaxString(1234567890));
 }
}