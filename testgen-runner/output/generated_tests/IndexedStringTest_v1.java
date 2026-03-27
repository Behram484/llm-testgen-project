package indexedstring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IndexedStringTest_v1 {
 
 @Test
 void testIndexOf() {
 // Create an instance of the class under test
 IndexedString indexedString = new IndexedString("Hello World");
 
 // Test normal case
 int expected = 4; // 'o' is at position 4 in "Hello"
 char[] target1 = {'o'};
 assertEquals(expected, indexedString.indexOf(target1));
 
 // Test case where the target string does not exist in the IndexedString
 int expected2 = -1; // There are no 'z's in "Hello"
 char[] target2 = {'z'};
 assertEquals(expected2, indexedString.indexOf(target2));
 
 // Test case where the target string is an empty character array
 int expected3 = 0; // The first character of any string is at position in "Hello World"
 char[] target3 = new char[0]; // Empty character array
 assertEquals(expected3, indexedString.indexOf(target3));
 }
}