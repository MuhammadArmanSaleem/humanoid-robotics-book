---
title: "Kinematics and Motion"
description: "Lesson 1 in Chapter 2: Fundamentals of Humanoid Robotics"
sidebar_position: 1
---

# ROS 2 Architecture & Core Concepts

## Introduction

Welcome to Lesson 1 of Chapter 2. In this lesson, you will learn about ROS 2 (Robot Operating System 2) architecture and core concepts, which form the foundation for modern humanoid robotics development. ROS 2 serves as middleware for robotics communication, providing a flexible framework for distributed computing in robotics applications. This lesson covers the publish-subscribe communication pattern, services and actions for synchronous/asynchronous operations, and Quality of Service (QoS) profiles essential for real-time robotics communication.

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand ROS 2 as middleware for robotics communication
- Apply publish-subscribe communication patterns in robotics applications
- Analyze Quality of Service (QoS) profiles and their applications in humanoid robotics

## Key Concepts

### Subsection 1: Core Principles

**ROS 2 as Middleware**: ROS 2 functions as middleware that provides a flexible framework for distributed computing in robotics applications. Unlike monolithic systems, ROS 2 enables modular development where different components can run on different machines and communicate seamlessly. This architecture is particularly important for humanoid robots where computational resources may be distributed across different hardware units.

**Publish-Subscribe Communication Pattern**: The publish-subscribe pattern is the primary communication mechanism in ROS 2. Publishers send messages to topics without knowing who will receive them, while subscribers receive messages from topics without knowing who sent them. This decoupling allows for flexible system architectures where components can be added, removed, or replaced without affecting the entire system.

**Services and Actions**: For synchronous operations, ROS 2 provides Services which follow a request-response pattern. For longer-running tasks with feedback, Actions provide a more sophisticated communication pattern that supports goals, feedback, and result messages. These are essential for humanoid robot control where some operations require immediate responses while others are ongoing processes.

### Subsection 2: Practical Applications

**Unitree H1**: The Unitree H1 humanoid robot utilizes ROS 2 for its control architecture, leveraging the publish-subscribe pattern for sensor data distribution and the action system for complex movement sequences. This allows for real-time control of the robot's 25+ degrees of freedom with precise timing and coordination.

**NASA Valkyrie**: NASA's humanoid robot for space applications uses ROS 2 to manage its complex sensor suite and control systems. The QoS profiles in ROS 2 ensure that critical sensor data and control commands are delivered with appropriate reliability and latency requirements.

**Agility Robotics Digit**: The Digit bipedal robot employs ROS 2 for coordinating its perception, planning, and control systems. The middleware architecture allows for rapid development and testing of different algorithms while maintaining system stability.

**Navigation2 (Nav2)**: The ROS 2-based navigation stack demonstrates how complex robotics systems can be built using the publish-subscribe architecture, with separate nodes handling localization, mapping, path planning, and motion control.

### Subsection 3: Advanced Considerations

**Quality of Service (QoS) Profiles**: QoS profiles in ROS 2 allow fine-tuning of communication behavior. For humanoid robots, different data types require different QoS settings - sensor data might need reliable delivery with low latency, while debugging information might tolerate occasional loss. Key QoS settings include reliability (reliable vs best-effort), durability (transient-local vs volatile), and deadline constraints.

**Real-time Performance Considerations**: For humanoid robot control, timing is critical. ROS 2 supports real-time systems through RTI Connext DDS and other middleware implementations that can guarantee message delivery within specified time constraints. This is essential for stable control of dynamic systems like humanoid robots.

**Security Features**: ROS 2 includes built-in security features including authentication, access control, and encryption, which are important for humanoid robots that may operate in sensitive environments or handle personal data.

## Hands-on Exercise

### Prerequisites
- ROS 2 Humble Hawksbill or later installed
- Basic knowledge of Linux command line
- Docker installed (optional, for containerized testing)

### Steps
1. Set up a basic ROS 2 workspace with a publisher and subscriber node
2. Create a custom message type for humanoid robot joint states
3. Implement a publisher that simulates joint position data (publishing at 100Hz)
4. Create a subscriber that processes the joint data and logs it
5. Configure QoS profiles to ensure reliable delivery for critical joint data
6. Implement a service client and server to demonstrate request-response communication
7. Add an action server to simulate a humanoid robot movement sequence

### Expected Outcome
After completing this exercise, you should have a working ROS 2 system with publisher-subscriber communication, services, and actions. You'll understand how to configure QoS settings for different types of robot data and how the middleware architecture enables modular robot software development.

## Quiz

1. **Question 1:** What is the primary communication mechanism in ROS 2?
   - A) Request-response pattern only
   - B) Publish-subscribe pattern
   - C) Direct function calls
   - D) File-based communication

2. **Question 2:** Which ROS 2 feature is best suited for long-running tasks with feedback?
   - A) Topics
   - B) Services
   - C) Actions
   - D) Parameters

3. **Question 3:** According to the lesson, which humanoid robot utilizes ROS 2 for its control architecture?
   - A) Boston Dynamics Atlas
   - B) Tesla Optimus
   - C) Unitree H1
   - D) Figure 01

### Quiz Answers
1. B) Publish-subscribe pattern
2. C) Actions
3. C) Unitree H1

## Key Takeaways

- ROS 2 serves as middleware that provides a flexible framework for distributed computing in robotics applications, essential for complex systems like humanoid robots
- The publish-subscribe communication pattern enables modular development where components can be added, removed, or replaced without affecting the entire system
- Quality of Service (QoS) profiles allow fine-tuning of communication behavior to meet the specific requirements of different types of robot data

## Further Reading

- ROS 2 official documentation: https://docs.ros.org/en/rolling/
- Navigation2 (Nav2) official documentation: https://navigation.ros.org/
- Quigley, M., et al. (2009). "ROS: an open-source robot operating system"
- ROS 2 source code and technical details: https://github.com/ros2/ros2

### Technical Deep Dive

### Real-time Performance in ROS 2

ROS 2 supports real-time systems through various DDS (Data Distribution Service) implementations like RTI Connext DDS, Eclipse Cyclone DDS, and Fast DDS. For humanoid robot control applications, real-time performance is critical as control loops often run at high frequencies (100Hz or higher) to maintain stability. The middleware must guarantee message delivery within specified time constraints to ensure stable control of dynamic systems.

### Middleware Comparison

While ROS 2 provides the standard middleware interface, different DDS implementations offer various performance characteristics suitable for different humanoid robot applications. RTI Connext DDS is often chosen for safety-critical applications, while Eclipse Cyclone DDS and Fast DDS provide good performance for research applications with lower licensing costs.

### Next Lesson
Continue to [Control Systems](./lesson-2-control-systems) to build upon the concepts learned in this lesson.