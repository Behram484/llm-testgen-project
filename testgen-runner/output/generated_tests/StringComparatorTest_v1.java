package stringcomparator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class StringComparatorTest_v1 {
 @Test
 void testCompareObjectMethod() {
 StringComparator comparator = new StringComparator();
 
 assertEquals(0, comparator.compare("abc", "abc"));
 assertThrows(ClassCastException.class, () -> comparator.compare(new Obje[4D[K
Object(), "test"));
 }
 
 @Test
 void testCompareStaticMethod() {
 assertEquals(0, StringComparator.compare("abc", "abc"));
 assertEquals(-1, StringComparator.compare("abc", "abcd"));
 assertEquals(+1, StringComparator.compare("abcd", "abc"));
 }
}