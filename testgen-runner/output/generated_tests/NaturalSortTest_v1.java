package naturalsort;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class NaturalSortTest_v1 {
 @Test
 public void testCompareIgnoreCase() {
 assertEquals(-1, NaturalSort.compareIgnoreCase("Photo 7.jpeg", "Photo 1[1D[K
17.jpeg"));
 }

 @Test
 public void testCompare() {
 assertEquals(0, NaturalSort.compare("123456", "123456"));
 assertThrows(NullPointerException.class, () -> NaturalSort.compare(null[24D[K
NaturalSort.compare(null, null));
 }
}