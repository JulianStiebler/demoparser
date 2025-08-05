from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

class DotSeparatedString(str):
    """
    A string that represents a dot-separated value.
    """
    @property
    def parts(self) -> list[str]:
        """Returns a list of strings split by the dot separator."""
        return self.split('.')

    def __repr__(self):
        return f"DotSeparatedString({super().__repr__()})"
    
@dataclass
class Header:
    server_name: str
    demo_file_stamp: str
    network_protocol: str
    map_name: str
    fullpackets_version: str
    allow_clientside_entities: str
    allow_clientside_particles: str
    demo_version_name: str
    demo_version_guid: str
    client_name: str
    game_directory: str
    addons: DotSeparatedString = field(default_factory=DotSeparatedString)

    @property
    def addons_list(self) -> List[str]:
        return self.addons.parts


@dataclass
class VoiceData:
    """
    Container for voice data from parse_voice().
    Maps Steam IDs to voice audio bytes.
    """
    voice_clips: dict[str, bytes]  # steamid -> audio bytes
    
    @property
    def player_count(self) -> int:
        """Number of players with voice data."""
        return len(self.voice_clips)
    
    @property
    def player_ids(self) -> List[str]:
        """List of Steam IDs with voice data."""
        return list(self.voice_clips.keys())
    
    @property
    def total_audio_size(self) -> int:
        """Total size of all voice clips in bytes."""
        return sum(len(clip) for clip in self.voice_clips.values())
    
    def get_player_voice(self, steamid: str) -> Optional[bytes]:
        """Get voice data for a specific player."""
        return self.voice_clips.get(steamid)
    
    def has_voice_data(self, steamid: str) -> bool:
        """Check if player has voice data."""
        return steamid in self.voice_clips

    def export_wav(self, steamid: str):
        try:
            import io
            from pydub import AudioSegment
        except ImportError:
            return

        clip_bytes = self.get_player_voice(steamid)
        if not clip_bytes:
            print(f"No voice data found for Steam ID: {steamid}")
            return

        try:
            audio_file = io.BytesIO(clip_bytes)
            audio_segment = AudioSegment.from_wav(audio_file)
            with open("test.wav", "wb") as temp_file:
                audio_segment.export(temp_file, format="wav")
            
        except Exception as e:
            print(f"Error playing audio for {steamid}: {e}")
# Auto-generated dataclasses for parsing methods

@dataclass
class PlayerInfo:
    """
    Auto-generated dataclass for Player Info Schema.
    """
    steamid: int  # Player Steam ID
    name: str  # Player name
    team_number: int  # Team number

@dataclass
class Grenade:
    """
    Auto-generated dataclass for Grenades Schema.
    """
    grenade_type: str  # Y coordinate
    grenade_entity_id: int  # Y coordinate
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate
    tick: int  # Game tick when event occurred
    steamid: int  # Player Steam ID
    name: str  # Player name

@dataclass
class Skin:
    """
    Auto-generated dataclass for Skins Schema.
    """
    def_index: int  # X coordinate
    item_id: int  # Item name
    paint_index: int  # Paint/skin index
    paint_seed: int  # Paint seed for pattern
    paint_wear: int  # Wear value of the skin
    custom_name: str  # Custom name tag
    steamid: int  # Player Steam ID

# Auto-generated dataclasses for events

@dataclass
class PlayerBlindEvent:
    """
    Auto-generated dataclass for player_blind event.
    """
    attacker_name: str  # Attacker name
    attacker_steamid: str  # Attacker Steam ID
    blind_duration: float  # Blind Duration
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class BombBeginplantEvent:
    """
    Auto-generated dataclass for bomb_beginplant event.
    """
    site: int  # Site
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class RoundTimeWarningEvent:
    """
    Auto-generated dataclass for round_time_warning event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class HegrenadeDetonateEvent:
    """
    Auto-generated dataclass for hegrenade_detonate event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class RoundAnnounceLastRoundHalfEvent:
    """
    Auto-generated dataclass for round_announce_last_round_half event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class CsRoundStartBeepEvent:
    """
    Auto-generated dataclass for cs_round_start_beep event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class PlayerJumpEvent:
    """
    Auto-generated dataclass for player_jump event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class PlayerTeamEvent:
    """
    Auto-generated dataclass for player_team event.
    """
    disconnect: bool  # Disconnect
    isbot: bool  # Isbot
    oldteam: int  # Oldteam
    silent: bool  # Silent
    team: int  # Team
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class ServerCvarEvent:
    """
    Auto-generated dataclass for server_cvar event.
    """
    name: str  # Player name
    tick: int  # Game tick when event occurred
    value: str  # Value

@dataclass
class RoundFreezeEndEvent:
    """
    Auto-generated dataclass for round_freeze_end event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class RoundAnnounceWarmupEvent:
    """
    Auto-generated dataclass for round_announce_warmup event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class HltvChaseEvent:
    """
    Auto-generated dataclass for hltv_chase event.
    """
    distance: int  # Distance
    inertia: int  # Inertia
    ineye: int  # Y coordinate
    phi: int  # Phi
    target1: int  # Target1
    target2: int  # Target2
    theta: int  # Theta
    tick: int  # Game tick when event occurred

@dataclass
class RoundOfficiallyEndedEvent:
    """
    Auto-generated dataclass for round_officially_ended event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class AnnouncePhaseEndEvent:
    """
    Auto-generated dataclass for announce_phase_end event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class BombDroppedEvent:
    """
    Auto-generated dataclass for bomb_dropped event.
    """
    entindex: int  # X coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class PlayerHurtEvent:
    """
    Auto-generated dataclass for player_hurt event.
    """
    armor: int  # Player armor
    attacker_name: str  # Attacker name
    attacker_steamid: str  # Attacker Steam ID
    dmg_armor: int  # Player armor
    dmg_health: int  # Player health
    health: int  # Player health
    hitgroup: str  # Hitgroup
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    weapon: str  # Weapon name

@dataclass
class PlayerDeathEvent:
    """
    Auto-generated dataclass for player_death event.
    """
    assistedflash: bool  # Assistedflash
    assister_name: str  # Player name
    assister_steamid: str  # Player Steam ID
    attacker_name: str  # Attacker name
    attacker_steamid: str  # Attacker Steam ID
    attackerblind: bool  # Attackerblind
    attackerinair: bool  # Attackerinair
    distance: float  # Distance
    dmg_armor: int  # Player armor
    dmg_health: int  # Player health
    dominated: int  # Dominated
    headshot: bool  # Whether it was a headshot
    hitgroup: str  # Hitgroup
    noreplay: bool  # Y coordinate
    noscope: bool  # Noscope
    penetrated: int  # Penetrated
    revenge: int  # Revenge
    thrusmoke: bool  # Thrusmoke
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    weapon: str  # Weapon name
    weapon_fauxitemid: str  # X coordinate
    weapon_itemid: str  # Weapon name
    weapon_originalowner_xuid: str  # X coordinate
    wipe: int  # Wipe

@dataclass
class InfernoStartburnEvent:
    """
    Auto-generated dataclass for inferno_startburn event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class BombPlantedEvent:
    """
    Auto-generated dataclass for bomb_planted event.
    """
    site: int  # Site
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class ItemPickupEvent:
    """
    Auto-generated dataclass for item_pickup event.
    """
    defindex: int  # Item definition index
    item: str  # Item name
    silent: bool  # Silent
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class RoundAnnounceMatchStartEvent:
    """
    Auto-generated dataclass for round_announce_match_start event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class ServerMessageEvent:
    """
    Auto-generated dataclass for server_message event.
    """
    server_message: str  # Server Message
    tick: int  # Game tick when event occurred

@dataclass
class DecoyDetonateEvent:
    """
    Auto-generated dataclass for decoy_detonate event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class HltvFixedEvent:
    """
    Auto-generated dataclass for hltv_fixed event.
    """
    fov: float  # Fov
    offset: int  # Offset
    phi: int  # Phi
    posx: int  # X coordinate
    posy: int  # Y coordinate
    posz: int  # Z coordinate
    target: int  # Target
    theta: int  # Theta
    tick: int  # Game tick when event occurred

@dataclass
class PlayerFootstepEvent:
    """
    Auto-generated dataclass for player_footstep event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class DecoyStartedEvent:
    """
    Auto-generated dataclass for decoy_started event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class WeaponFireEvent:
    """
    Auto-generated dataclass for weapon_fire event.
    """
    silenced: bool  # Silenced
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    weapon: str  # Weapon name

@dataclass
class OtherDeathEvent:
    """
    Auto-generated dataclass for other_death event.
    """
    attacker_name: str  # Attacker name
    attacker_steamid: str  # Attacker Steam ID
    attackerblind: bool  # Attackerblind
    headshot: bool  # Whether it was a headshot
    noscope: bool  # Noscope
    otherid: int  # Otherid
    othertype: str  # Y coordinate
    penetrated: int  # Penetrated
    thrusmoke: bool  # Thrusmoke
    tick: int  # Game tick when event occurred
    weapon: str  # Weapon name
    weapon_fauxitemid: str  # X coordinate
    weapon_itemid: str  # Weapon name
    weapon_originalowner_xuid: str  # X coordinate

@dataclass
class CsPreRestartEvent:
    """
    Auto-generated dataclass for cs_pre_restart event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class BombPickupEvent:
    """
    Auto-generated dataclass for bomb_pickup event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class InfernoExpireEvent:
    """
    Auto-generated dataclass for inferno_expire event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class BombExplodedEvent:
    """
    Auto-generated dataclass for bomb_exploded event.
    """
    site: int  # Site
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class RoundPrestartEvent:
    """
    Auto-generated dataclass for round_prestart event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class FlashbangDetonateEvent:
    """
    Auto-generated dataclass for flashbang_detonate event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class BombBegindefuseEvent:
    """
    Auto-generated dataclass for bomb_begindefuse event.
    """
    haskit: bool  # Haskit
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class SmokegrenadeDetonateEvent:
    """
    Auto-generated dataclass for smokegrenade_detonate event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class SmokegrenadeExpiredEvent:
    """
    Auto-generated dataclass for smokegrenade_expired event.
    """
    entityid: int  # Y coordinate
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    x: float  # X coordinate
    y: float  # Y coordinate
    z: float  # Z coordinate

@dataclass
class CsWinPanelMatchEvent:
    """
    Auto-generated dataclass for cs_win_panel_match event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class ChatMessageEvent:
    """
    Auto-generated dataclass for chat_message event.
    """
    chat_message: str  # Chat Message
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class CsRoundFinalBeepEvent:
    """
    Auto-generated dataclass for cs_round_final_beep event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class PlayerSpawnEvent:
    """
    Auto-generated dataclass for player_spawn event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class BombDefusedEvent:
    """
    Auto-generated dataclass for bomb_defused event.
    """
    site: int  # Site
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class PlayerDisconnectEvent:
    """
    Auto-generated dataclass for player_disconnect event.
    """
    PlayerID: int  # Y coordinate
    name: str  # Player name
    networkid: str  # Networkid
    reason: int  # Reason
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    xuid: int  # X coordinate

@dataclass
class RoundPoststartEvent:
    """
    Auto-generated dataclass for round_poststart event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class WeaponReloadEvent:
    """
    Auto-generated dataclass for weapon_reload event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class RoundAnnounceMatchPointEvent:
    """
    Auto-generated dataclass for round_announce_match_point event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class BeginNewMatchEvent:
    """
    Auto-generated dataclass for begin_new_match event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class BuytimeEndedEvent:
    """
    Auto-generated dataclass for buytime_ended event.
    """
    tick: int  # Game tick when event occurred

@dataclass
class WeaponZoomEvent:
    """
    Auto-generated dataclass for weapon_zoom event.
    """
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID

@dataclass
class ItemEquipEvent:
    """
    Auto-generated dataclass for item_equip event.
    """
    canzoom: bool  # Z coordinate
    defindex: int  # Item definition index
    hassilencer: bool  # Hassilencer
    hastracers: bool  # Hastracers
    ispainted: bool  # Ispainted
    issilenced: bool  # Issilenced
    item: str  # Item name
    tick: int  # Game tick when event occurred
    user_name: str  # Player name
    user_steamid: str  # Player Steam ID
    weptype: int  # Y coordinate

