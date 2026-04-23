package indexedstring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class IndexedStringTest_v1 {

 @Test
 void testIndexOf() {
 IndexedString indexedString = new IndexedString("hello");
 char[] target = {'e', 'l'};
 assertEquals(1, indexedString.indexOf(target));
 }

 @Test
 void testIndexOfNotFound() {
 IndexedString indexedString = new IndexedString("hello");
 char[] target = {'z'};
 assertEquals(-1, indexedString.indexOf(target));
 }
}