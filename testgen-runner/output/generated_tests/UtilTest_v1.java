package util;

import org.junit.jupiter.api.Test;
import java.util.Vector;
import static org.junit.jupiter.api.Assertions.*;

public class UtilTest_v1 {
 private final Util util = new Util(); // Create an instance of the Uti[3D[K
Util class

 @Test
 void testStringIsEmpty() {
 assertTrue(Util.StringIsEmpty(""));
 assertFalse(Util.StringIsEmpty("Not Empty"));
 assertTrue(Util.StringIsEmpty(null));
 }

 @Test
 void testNormalizeString() {
 assertEquals("", Util.NormalizeString(null));
 assertEquals("Non-Null String", Util.NormalizeString("Non-Null Stri[4D[K
String"));
 }

 // Same with your original code, only change is to call methods on the [K
instance 'util' instead of calling them statically
 @Test
 void testIntMaxString() {
 assertEquals("", Util.IntMaxString(Integer.MAX_VALUE));
 assertEquals("1234567890", Util.IntMaxString(1234567890));
 }
}