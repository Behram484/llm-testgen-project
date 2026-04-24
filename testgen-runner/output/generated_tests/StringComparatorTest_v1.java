package corina.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class StringComparatorTest_v1 {
 @Test
 void testCompareObjects() {
 Comparator<Object> comparator = new StringComparator();
 
 assertEquals(0, comparator.compare("test", "test"));
 assertEquals(-1, comparator.compare("apple", "banana"));
 assertEquals(+1, comparator.compare("banana", "apple"));
 }

 @Test
 void testCompareStatic() {
 assertEquals(0, StringComparator.compare("test", "test"));
 assertEquals(-1, StringComparator.compare("apple", "banana"));
 assertEquals(+1, StringComparator.compare("banana", "apple"));
 }
}