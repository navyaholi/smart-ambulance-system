# System Architecture

## Overview

The Smart Ambulance System is divided into separate modules.

```text
User / Client
      |
      v
Application Layer
      |
      +------------------+
      |                  |
      v                  v
Algorithms          Allocation
      |                  |
      +--------+---------+
               |
               v
          Data Models
               |
               v
          JSON Data