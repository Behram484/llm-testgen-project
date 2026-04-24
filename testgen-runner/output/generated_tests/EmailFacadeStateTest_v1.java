package ch.bluepenguin.email.client.service.impl;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class EmailFacadeStateTest_v1 {
 private EmailFacadeState emailFacadeState;
 
 @BeforeEach
 void setUp() {
 // Arrange: Setup the test fixture before every test method runs
 emailFacadeState = new EmailFacadeState();
 }
 
 @Test
 void testSetAndGetState_withValidParameters() {
 // Act and Assert: Test setting a state and then getting it back
 Integer ID = 1;
 boolean dirtyFlag = true;
 emailFacadeState.setState(ID, dirtyFlag);
 assertFalse(emailFacadeState.isDirty(2)); 
 assertTrue(emailFacadeState.isDirty(ID)); 
 }
 
 @Test
 void testClear() {
 // Arrange: Setup a non-empty state first
 emailFacadeState.setState(1, false);
 emailFacadeState.setState(2, true);
 
 // Act: Clear the states
 emailFacadeState.clear();
 
 // Assert: All IDs should return true as they are all default dirty[5D[K
dirty states
 assertTrue(emailFacadeState.isDirty(1)); 
 assertTrue(emailFacadeState.isDirty(2)); 
 }
 
 @Test
 void testSetAllAndIsAllClean() {
 // Arrange: Setup a non-empty state first
 emailFacadeState.setState(1, false);
 emailFacadeState.setState(2, true);
 
 // Act and Assert: Test setting all states to the same value and ch[2D[K
checking if they are clean
 boolean dirtyFlag = false;
 emailFacadeState.setAll(dirtyFlag);
 assertTrue(emailFacadeState.isDirty(1)); 
 assertFalse(emailFacadeState.isDirty(2)); 
 
 // Assert: Check if all states are clean after setting them to fals[4D[K
false
 assertTrue(emailFacadeState.isAllClean()); 
 }
}