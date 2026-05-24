# 🚲 Bike Security & Emergency Alert System

## 📌 Overview

Bike Security & Emergency Alert System is a blockchain-based project designed to improve bike safety and emergency response. The system helps users monitor their bikes, detect suspicious activities or accidents, and securely store alert information using blockchain technology.

The project integrates smart contracts, MetaMask, Ganache, and web technologies to provide secure, transparent, and tamper-proof data handling.

---

## 🚀 Features

* 🔐 User authentication using MetaMask
* 🚲 Bike registration and monitoring
* 🚨 Automatic accident/tampering detection
* 📢 Manual emergency alert system
* ⛓️ Blockchain-based secure record storage
* 🔒 Tamper-proof transaction history
* 💻 Beginner-friendly web interface

---

## 🧠 Problem Statement

Traditional bike security and emergency systems mainly depend on manual reporting, which can delay emergency response. In many situations, victims may not be able to ask for help due to injuries or unconsciousness.

This project aims to solve this problem by automatically detecting emergencies and securely storing alert data using blockchain technology.

---

## 🎯 Objectives

* Detect suspicious activities and accidents automatically
* Reduce emergency response time
* Provide secure and transparent data storage
* Prevent modification of emergency records
* Create an easy-to-use safety platform

---

## 🛠️ Tech Stack

| Technology          | Purpose               |
| ------------------- | --------------------- |
| HTML/CSS/JavaScript | Frontend              |
| React.js            | User Interface        |
| Node.js             | Backend               |
| Solidity            | Smart Contracts       |
| Ganache             | Local Blockchain      |
| MetaMask            | Wallet Authentication |
| Ethereum Blockchain | Secure Data Storage   |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/prasan474/BikeSecurityDPP.git
cd BikeSecurityDPP
```

### 2️⃣ Install Dependencies

```bash
npm install
```

### 3️⃣ Install Ganache

Ganache is used to run a local Ethereum blockchain for development and testing.

Download Ganache from:
https://trufflesuite.com/ganache/

After installation:

* Open Ganache
* Create a new workspace
* Start the local blockchain

Default RPC URL:

```bash
http://127.0.0.1:7545
```

---

### 4️⃣ Setup MetaMask

MetaMask is required for blockchain authentication and transaction approval.

Install MetaMask extension:
https://metamask.io/

Add a custom Ganache network using:

| Field           | Value                 |
| --------------- | --------------------- |
| Network Name    | Ganache Local         |
| RPC URL         | http://127.0.0.1:7545 |
| Chain ID        | 1337                  |
| Currency Symbol | ETH                   |

Import an account using the private key provided by Ganache.

---

### 5️⃣ Compile Smart Contracts

```bash
truffle compile
```

---

### 6️⃣ Deploy Smart Contracts

```bash
truffle migrate
```

---

### 7️⃣ Run the Application

```bash
npm start
```

If the above command does not work, try:

```bash
npm run dev
```

---

## 📂 Project Structure

```plaintext
BikeSecurityDPP/
│── contracts/        # Smart contracts
│── migrations/       # Contract deployment scripts
│── src/              # Frontend source code
│── public/           # Static files
│── README.md
```

---

## 🔄 Working Flow

1. User registers and connects MetaMask wallet
2. Bike details are added to the system
3. Sensors monitor bike activity
4. Emergency alerts are triggered during suspicious activity
5. Alert information is stored securely on blockchain
6. Users can also manually trigger alerts

---

## 🌍 Future Scope

* 📍 GPS tracking support
* 🚑 Automatic ambulance notification
* 📱 Mobile application integration
* 🏙️ Smart city integration
* 👮 Emergency service connectivity

---

## 🤝 Contribution Guidelines

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Make your changes
4. Commit changes

```bash
git commit -m "Improved README documentation"
```

5. Push changes

```bash
git push origin feature-name
```

6. Create a Pull Request

---

## 🐞 Reporting Issues

If you find any bugs or issues:

* Open an issue
* Describe the problem clearly
* Add screenshots if possible

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙌 Acknowledgements

* Ethereum Blockchain
* MetaMask
* Ganache
* Open Source Community
