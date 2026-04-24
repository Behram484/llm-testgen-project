package de.beiri22.stringincrementor.relativestring;

import org.junit.jupiter.api.Test;
import java.nio.ByteBuffer;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class StringLinkTest_v1 {
 @Test
 void testToBytes() {
 // Arrange
 int posOrig = 3;
 int posNew = 4;
 int len = 5;
 StringLink stringLink = new StringLink(posOrig, posNew, len);
 
 // Act
 byte[] bytes = stringLink.toBytes();
 ByteBuffer buffer = ByteBuffer.wrap(bytes);
 
 // Assert
 assertEquals(len, buffer.getInt());
 assertEquals(posOrig, buffer.getInt());
 assertEquals(posNew, buffer.getInt());
 }

 // Passing tests remain unchanged
}