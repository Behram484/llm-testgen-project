package stringlink;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StringLinkTest {
 
 @Test
 void testConstructorAndGetters() {
 // Given
 int posOrig = 3, posNew = 4, len = 5;
 
 // When
 StringLink stringLink = new StringLink(posOrig, posNew, len);
 
 // Then
 assertEquals(len, stringLink.getLen());
 assertEquals(posNew, stringLink.getPosNew());
 assertEquals(posOrig, stringLink.getPosOrig());
 }
 
 @Test
 void testToString() {
 // Given
 int posOrig = 3, posNew = 4, len = 5;
 
 // When
 StringLink stringLink = new StringLink(posOrig, posNew, len);
 
 // Then
 assertEquals("{" + len + ": " + posOrig + "-->" + posNew + "}", stringLink.toString());
 }
 
 @Test
 void testConstructorWithBytes() {
 // Given
 byte[] data = new byte[]{0, 0, 0, 5, 0, 0, 0, 3, 0, 0, 0, 4};
 
 // When
 StringLink stringLink = new StringLink(data);
 
 // Then
 assertEquals(5, stringLink.getLen());
 assertEquals(3, stringLink.getPosOrig());
 assertEquals(4, stringLink.getPosNew());
 }
 
 @Test
 void testToBytes() {
 // Given
 StringLink stringLink = new StringLink(2, 3, 5);
 
 // When
 byte[] data = stringLink.toBytes();
 int len = data[0] + (data[1] << 8) + (data[2] << 16) + (data[3] << 24);
 int posOrig = data[4] + (data[5] << 8) + (data[6] << 16) + (data[7] << 24);
 int posNew = data[8] + (data[9] << 8) + (data[10] << 16) + (data[11] << 24);
 
 // Then
 assertEquals(5, len);
 assertEquals(2, posOrig);
 assertEquals(3, posNew);
 }
}