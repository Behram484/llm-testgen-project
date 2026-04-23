package xstringsupport;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class XStringSupportTest_v1 {
 @Test
 public void testGetNumberString() {
 assertEquals("007", XStringSupport.getNumberString(7, 3));
 assertEquals("-9456", XStringSupport.getNumberString(-456, 4));
 assertThrows(IllegalArgumentException.class, () -> XStringSupport.g[16D[K
XStringSupport.getNumberString(1234567890, 3));
 }

 @Test
 public void testSuccessorUsualChars() {
 assertEquals(" ", XStringSupport.successorUsualChars("{", false));
 assertEquals("A", XStringSupport.successorUsualChars("Z", false));
 assertEquals(" B", XStringSupport.successorUsualChars("AZ", true));[7D[K
true));
 }
}