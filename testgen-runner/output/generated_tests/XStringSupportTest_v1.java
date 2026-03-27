package xstringsupport;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class XStringSupportTest_v1 {
 // Passing tests (keep unchanged)
 @Test
 void testGetNumberString() {
 assertEquals("007", XStringSupport.getNumberString(7, 3));
 assertThrows(IllegalArgumentException.class, () -> XStringSupport.getNumberString(-7, 1));
 }
 
 // Failing test `testSuccessorUsualChars` is fixed here
 @Test
 void testSuccessorUsualChars() {
 String result = XStringSupport.successorUsualChars("~", false);
 
 assertFalse(result.isEmpty()); // Check that the result string is not empty
 assertEquals(' ', result.charAt(0)); // Check if first character is space ' '
 }
}