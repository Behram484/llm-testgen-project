package corina.util;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

public class NaturalSortTest_v1 {
 @Test
 void testCompareNormal() {
 assertEquals(-1, NaturalSort.compare("Photo 7.jpeg", "Photo 17.jpeg[7D[K
17.jpeg"));
 assertEquals(0, NaturalSort.compare("Photo 17.jpeg", "Photo 17.jpeg[7D[K
17.jpeg"));
 assertEquals(+1, NaturalSort.compare("Photo 27.jpeg", "Photo 17.jpe[6D[K
17.jpeg"));
 }

 @Test
 void testCompareIgnoreCaseNormal() {
 assertEquals(-1, NaturalSort.compareIgnoreCase("Photo 7.jpeg", "Pho[4D[K
"Photo 17.jpeg"));
 assertEquals(0, NaturalSort.compareIgnoreCase("Photo 17.jpeg", "Pho[4D[K
"Photo 17.jpeg"));
 assertEquals(+1, NaturalSort.compareIgnoreCase("Photo 27.jpeg", "Ph[3D[K
"Photo 17.jpeg"));
 }

 @Test
 void testCompareDifferentCases() {
 assertEquals(-1, NaturalSort.compare("photo 7.jpeg", "PHOTO 17.jpeg[7D[K
17.jpeg"));
 assertEquals(0, NaturalSort.compare("photo 17.jpeg", "Photo 17.jpeg[7D[K
17.jpeg"));
 assertEquals(+1, NaturalSort.compare("pHoTo 27.jpeg", "PhoTO 17.jpe[6D[K
17.jpeg"));
 }

 @Test
 void testCompareIgnoreCaseDifferentCases() {
 assertEquals(-1, NaturalSort.compareIgnoreCase("photo 7.jpeg", "PHO[4D[K
"PHOTO 17.jpeg"));
 assertEquals(0, NaturalSort.compareIgnoreCase("photo 17.jpeg", "Pho[4D[K
"Photo 17.jpeg"));
 assertEquals(+1, NaturalSort.compareIgnoreCase("pHoTo 27.jpeg", "Ph[3D[K
"PhoTO 17.jpeg"));
 }
}