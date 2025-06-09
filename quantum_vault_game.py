#!/usr/bin/env python3
"""
Quantum Vault: 타임루프 퍼즐 어드벤처 게임
2049년, 30분마다 초기화되는 양자 금고 속에서 단 하나의 미래를 뚫어라.
당신의 기억만이 세계 붕괴를 막는 키다.
"""

import os
import time
import random
import json
import sys
import curses
from typing import Dict, List, Any, Optional
from curses import wrapper

class QuantumVaultGame:
    def __init__(self):
        self.player_name = "Cipher Runner"
        self.current_loop = 1
        self.max_loops = 10
        self.alarms_triggered = 0
        self.collected_codes = []
        self.discovered_clues = {}
        self.game_state = "running"
        self.current_location = "entrance"
        self.inventory = []
        self.selected_option = 0
        
        # 게임 데이터 로드
        self.locations = self._load_locations()
        self.puzzles = self._load_puzzles()
        self.shift_codes = self._load_shift_codes()
        
        # ASCII 아트 로드
        self.ascii_art = self._load_ascii_art()
    
    def _load_ascii_art(self) -> Dict:
        """ASCII 아트 로드"""
        return {
            "title": """
  ██████  ██    ██  █████  ███    ██ ████████ ██    ██ ███    ███ 
 ██    ██ ██    ██ ██   ██ ████   ██    ██    ██    ██ ████  ████ 
 ██    ██ ██    ██ ███████ ██ ██  ██    ██    ██    ██ ██ ████ ██ 
 ██ ▄▄ ██ ██    ██ ██   ██ ██  ██ ██    ██    ██    ██ ██  ██  ██ 
  ██████   ██████  ██   ██ ██   ████    ██     ██████  ██      ██ 
     ▀▀                                                           
                         ██    ██  █████  ██    ██ ██   ████████  
                         ██    ██ ██   ██ ██    ██ ██      ██     
                         ██    ██ ███████ ██    ██ ██      ██     
                          ██  ██  ██   ██ ██    ██ ██      ██     
                           ████   ██   ██  ██████  ███████ ██     
            """,
            "vault": """
              ╔════════════════════════════════╗
              ║                                ║
              ║     ╔══════════════════╗       ║
              ║     ║                  ║       ║
              ║     ║   QUANTUM VAULT  ║       ║
              ║     ║                  ║       ║
              ║     ╚══════════════════╝       ║
              ║          ╔══════╗              ║
              ║          ║ ◯◯◯◯ ║              ║
              ║          ╚══════╝              ║
              ║                                ║
              ╚════════════════════════════════╝
            """,
            "eva": """
               ╔═══════════════════╗
               ║     ╭─────╮       ║
               ║     │ EVA │       ║
               ║     ╰─────╯       ║
               ║  ╭───────────╮    ║
               ║  │ ▓▓▓▓▓▓▓▓▓ │    ║
               ║  │ ▓▓▓▓▓▓▓▓▓ │    ║
               ║  │ ▓▓▓▓▓▓▓▓▓ │    ║
               ║  ╰───────────╯    ║
               ╚═══════════════════╝
            """,
            "alarm": """
               ╔═══════════════════╗
               ║    ⚠  ALERT  ⚠    ║
               ║                   ║
               ║  INTRUDER DETECTED║
               ║                   ║
               ║  SECURITY LEVEL:  ║
               ║     [▓▓▓▓▓]      ║
               ║                   ║
               ╚═══════════════════╝
            """,
            "game_over": """
              ╔════════════════════════════════╗
              ║                                ║
              ║          GAME  OVER            ║
              ║                                ║
              ║      QUANTUM LOOP FAILED       ║
              ║                                ║
              ╚════════════════════════════════╝
            """,
            "success": """
              ╔════════════════════════════════╗
              ║                                ║
              ║        MISSION SUCCESS         ║
              ║                                ║
              ║      QUANTUM VAULT OPENED      ║
              ║                                ║
              ╚════════════════════════════════╝
            """
        }
    
    def _load_locations(self) -> Dict:
        """게임 위치 데이터 로드"""
        # 실제 구현에서는 외부 JSON 파일에서 로드할 수 있음
        return {
            "entrance": {
                "name": "금고 입구",
                "description": "ZeitBank의 양자 금고 입구. 보안 스캐너와 EVA 터미널이 보인다.",
                "connections": ["security_hall", "monitoring_room"],
                "items": ["security_badge"],
                "ascii_art": """
                    ╔══════════════════╗
                    ║   ZEITBANK       ║
                    ║   ENTRANCE       ║
                    ╚══════════════════╝
                    │    │    │    │   │
                    │    │    │    │   │
                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                """
            },
            "security_hall": {
                "name": "보안 복도",
                "description": "레이저 센서와 모션 감지기가 설치된 좁은 복도.",
                "connections": ["entrance", "main_vault"],
                "items": [],
                "ascii_art": """
                    ╔══════════════════╗
                    ║ ╱╲  ╱╲  ╱╲  ╱╲  ║
                    ║ ╲╱  ╲╱  ╲╱  ╲╱  ║
                    ║                  ║
                    ║ <<<<< LASERS >>> ║
                    ╚══════════════════╝
                """
            },
            "monitoring_room": {
                "name": "모니터링 룸",
                "description": "금고 전체를 감시하는 화면들이 벽을 채우고 있다.",
                "connections": ["entrance", "server_room"],
                "items": ["access_card"],
                "ascii_art": """
                    ╔══════════════════╗
                    ║ ▓▓▓  ▓▓▓  ▓▓▓   ║
                    ║ ▓▓▓  ▓▓▓  ▓▓▓   ║
                    ║                  ║
                    ║ ▓▓▓  ▓▓▓  ▓▓▓   ║
                    ╚══════════════════╝
                """
            },
            "main_vault": {
                "name": "메인 금고",
                "description": "Chrono-Vault Core가 중앙에 빛나고 있다.",
                "connections": ["security_hall", "quantum_core"],
                "items": ["encryption_key"],
                "ascii_art": """
                    ╔══════════════════╗
                    ║                  ║
                    ║    ╔════════╗    ║
                    ║    ║  CORE  ║    ║
                    ║    ╚════════╝    ║
                    ╚══════════════════╝
                """
            },
            "server_room": {
                "name": "서버실",
                "description": "EVA의 주 서버가 위치한 차가운 방.",
                "connections": ["monitoring_room"],
                "items": ["system_log"],
                "ascii_art": """
                    ╔══════════════════╗
                    ║ ║║║║  ║║║║  ║║║║ ║
                    ║ ║║║║  ║║║║  ║║║║ ║
                    ║                  ║
                    ║ ║║║║  ║║║║  ║║║║ ║
                    ╚══════════════════╝
                """
            },
            "quantum_core": {
                "name": "양자 코어실",
                "description": "시간 루프의 중심. 불안정한 에너지가 공기를 진동시킨다.",
                "connections": ["main_vault"],
                "items": ["voss_message"],
                "ascii_art": """
                    ╔══════════════════╗
                    ║       ╱╲         ║
                    ║      ╱  ╲        ║
                    ║     ╱ ◯◯ ╲       ║
                    ║     ╲    ╱       ║
                    ╚══════════════════╝
                """
            }
        }
    
    def _load_puzzles(self) -> Dict:
        """퍼즐 데이터 로드"""
        return {
            "terminal_hack": {
                "name": "EVA 터미널 해킹",
                "description": "접근 코드를 찾아 EVA 터미널에 접속하세요.",
                "solution": "QUANTUM",
                "reward": "access_code_alpha",
                "difficulty": 1
            },
            "laser_grid": {
                "name": "레이저 그리드 우회",
                "description": "패턴을 분석해 레이저 그리드를 통과하세요.",
                "solution": "3-1-4-1-5-9",
                "reward": "security_override",
                "difficulty": 2
            }
        }
    
    def _load_shift_codes(self) -> Dict:
        """시프트 코드 데이터 로드"""
        return {
            "Δ-7F": {
                "location": "monitoring_room",
                "clue": "모니터 뒤 숨겨진 패널에서 발견",
                "story": "Voss의 첫 번째 경고 메시지"
            },
            "Ω-3D": {
                "location": "server_room",
                "clue": "서버 로그에서 발견된 암호화된 시퀀스",
                "story": "Nimbus의 계획 일부"
            }
        }
    
    def start_game(self):
        """게임 시작"""
        self._clear_screen()
        self._show_intro()
        
        while self.game_state == "running" and self.current_loop <= self.max_loops:
            self._game_loop()
            
        self._show_ending()
    
    def _clear_screen(self):
        """화면 지우기"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _show_intro(self):
        """게임 인트로 표시"""
        print("=" * 60)
        print("               QUANTUM VAULT               ")
        print("=" * 60)
        print("\n2049년, 30분마다 초기화되는 양자 금고 속에서")
        print("단 하나의 미래를 뚫어라.")
        print("당신의 기억만이 세계 붕괴를 막는 키다.\n")
        print("당신은 Cipher Runner, 루프 간 기억을 보존할 수 있는 유일한 해커다.")
        print("ZeitBank의 Shattered Vault에 침입해 세계 금융망 붕괴를 막아야 한다.")
        print("10번의 루프 안에 모든 시프트 코드를 모아 금고를 해제하라.\n")
        print("=" * 60)
        input("\n[Enter 키를 눌러 시작]")
    
    def _game_loop(self):
        """게임의 주요 루프"""
        self._clear_screen()
        print(f"\n===== 루프 {self.current_loop}/{self.max_loops} =====")
        print(f"현재 위치: {self.locations[self.current_location]['name']}")
        print(f"알람 상태: {'🔴' * self.alarms_triggered + '⚪' * (5 - self.alarms_triggered)}")
        print(f"수집한 시프트 코드: {len(self.collected_codes)}/10")
        
        print("\n" + self.locations[self.current_location]["description"])
        
        # 현재 위치의 아이템 표시
        items = self.locations[self.current_location]["items"]
        if items:
            print("\n이곳에서 발견할 수 있는 것들:")
            for item in items:
                print(f"- {item}")
        
        # 연결된 장소 표시
        connections = self.locations[self.current_location]["connections"]
        print("\n이동 가능한 장소:")
        for i, conn in enumerate(connections, 1):
            print(f"{i}. {self.locations[conn]['name']}")
        
        # 사용자 입력 처리
        print("\n행동을 선택하세요:")
        print("1-N. 장소로 이동")
        print("i. 인벤토리 확인")
        print("c. 단서 목록 확인")
        print("p. 퍼즐 풀기")
        print("q. 게임 종료")
        
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            self.game_state = "quit"
        elif choice == 'i':
            self._show_inventory()
        elif choice == 'c':
            self._show_clues()
        elif choice == 'p':
            self._solve_puzzle()
        elif choice.isdigit() and 1 <= int(choice) <= len(connections):
            self.current_location = connections[int(choice) - 1]
        else:
            print("잘못된 선택입니다.")
            time.sleep(1)
        
        # 루프 종료 조건 체크
        if random.random() < 0.2:  # 20% 확률로 EVA가 감지
            self._eva_detection()
    
    def _show_inventory(self):
        """인벤토리 표시"""
        self._clear_screen()
        print("\n===== 인벤토리 =====")
        if not self.inventory:
            print("인벤토리가 비어있습니다.")
        else:
            for item in self.inventory:
                print(f"- {item}")
        input("\n[Enter 키를 눌러 계속]")
    
    def _show_clues(self):
        """발견한 단서 표시"""
        self._clear_screen()
        print("\n===== 발견한 단서 =====")
        if not self.discovered_clues:
            print("아직 단서를 발견하지 못했습니다.")
        else:
            for clue, info in self.discovered_clues.items():
                print(f"- {clue}: {info}")
        input("\n[Enter 키를 눌러 계속]")
    
    def _solve_puzzle(self):
        """퍼즐 풀기 시도"""
        # 현재 위치에 따른 퍼즐 제공 로직 구현
        self._clear_screen()
        print("\n현재 위치에서는 풀 수 있는 퍼즐이 없습니다.")
        input("\n[Enter 키를 눌러 계속]")
    
    def _eva_detection(self):
        """EVA의 탐지 이벤트"""
        self._clear_screen()
        print("\n⚠️ 경고! EVA가 침입자를 감지했습니다! ⚠️")
        print("시스템이 30초 후 리셋됩니다...")
        self.alarms_triggered += 1
        
        if self.alarms_triggered >= 5:
            print("\nEVA 보안 프로토콜이 최고 수준으로 격상되었습니다.")
            print("루프를 강제로 재시작합니다.")
            self.current_loop += 1
            self.alarms_triggered = 0
        
        time.sleep(3)
    
    def _show_ending(self):
        """게임 엔딩 표시"""
        self._clear_screen()
        print("\n===== 게임 종료 =====")
        
        if self.game_state == "quit":
            print("게임을 종료했습니다.")
        elif len(self.collected_codes) >= 10:
            print("축하합니다! 모든 시프트 코드를 수집하여 금고를 해제했습니다.")
            print("세계 금융망이 안정화되었고, 당신은 영웅이 되었습니다.")
        elif self.current_loop > self.max_loops:
            print("10번의 루프가 모두 지났지만 금고를 해제하지 못했습니다.")
            print("세계 금융망이 붕괴되기 시작합니다...")
        
        print("\n게임을 플레이해 주셔서 감사합니다!")

if __name__ == "__main__":
    game = QuantumVaultGame()
    game.start_game()
