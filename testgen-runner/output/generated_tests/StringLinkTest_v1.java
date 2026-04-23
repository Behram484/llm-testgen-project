package stringlink;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class StringLinkTest_v1 {
 @Test
 void testStringLinkIntIntInt() {
 // Given
 int posOrig = 5;
 int posNew = 3;
 int len = 7;

 // When
 StringLink stringLink = new StringLink(posOrig, posNew, len);

 // Then
 assertEquals(len, stringLink.getLen());
 assertEquals(posOrig, stringLink.getPosOrig());
 assertEquals(posNew, stringLink.getPosNew());
 }

 @Test
 void testStringLinkByteArray() {
 // Given
 byte[] data = new byte[]{0x07, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, (byt[4D[K
(byte)0x00, (byte)0x03};

 // When
 StringLink stringLink = new StringLink(data);

 // Then
 assertEquals(7, stringLink.getLen());
 assertEquals(5, stringLink.getPosOrig());
 assertEquals(3, stringLink.getPosNew());
 }

 @Test
 void testToString() {
 // Given
 StringLink stringLink = new StringLink(5, 3, 7);

 // When
 String result = stringLink.toString();

 // Then
 assertEquals("{7: 5-->3}", result);
 }

 @Test
 void testToBytes() {
 // Given
 StringLink stringLink = new StringLink(5, 3, 7);

 // When
 byte[] result = stringLink.toBytes();

 // Then
 assertArrayEquals(new byte[]{0x07, 0x00, 0x00, 0x00, 0x05, 0x00, (byte)[6D[K
(byte)0x00, (byte)0x00, (byte)0x03}, result);
 }
}