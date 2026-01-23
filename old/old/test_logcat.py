"""
Script de validação da estrutura Logcat.

Testa importações básicas e estrutura de arquivos.
"""
import sys
from pathlib import Path

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("Testing Logcat module structure...")
    
    # Adicionar raiz do plugin ao path
    plugin_root = Path(__file__).parent.parent
    sys.path.insert(0, str(plugin_root))
    
    try:
        from plugins.logcat.core.model.log_entry import LogEntry
        print("✓ LogEntry")
        
        from plugins.logcat.core.model.log_session import LogSession
        print("✓ LogSession")
        
        from plugins.logcat.core.model.log_session_manager import LogSessionManager
        print("✓ LogSessionManager")
        
        from plugins.logcat.core.io.log_loader import LogLoader
        print("✓ LogLoader")
        
        from plugins.logcat.core.io.log_file_watcher import LogFileWatcher
        print("✓ LogFileWatcher")
        
        from plugins.logcat.core.filter.log_filter_engine import LogFilterEngine
        print("✓ LogFilterEngine")
        
        from plugins.logcat.core.color.class_color_provider import ClassColorProvider
        print("✓ ClassColorProvider")
        
        from plugins.logcat.core.color.tool_key_color_provider import ToolKeyColorProvider
        print("✓ ToolKeyColorProvider")
        
        print("\n✓ All imports successful!")
        return True
    
    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_log_entry():
    """Testa LogEntry com dados de exemplo."""
    print("\nTesting LogEntry functionality...")
    
    try:
        from plugins.logcat.core.model.log_entry import LogEntry
        
        # Criar entrada de teste
        json_line = '{"ts": "2026-01-22T11:28:52", "level": "INFO", "plugin": "MTL Tools", "tool": "system", "class": "TestClass", "msg": "Test message", "data": {}}'
        
        entry = LogEntry.from_json_line(json_line, 1)
        assert entry is not None
        assert entry.level == "INFO"
        assert entry.tool == "system"
        print("✓ LogEntry.from_json_line() works")
        
        short_msg = entry.get_short_message(50)
        assert len(short_msg) <= 50
        print("✓ LogEntry.get_short_message() works")
        
        print("✓ LogEntry tests passed!")
        return True
    
    except Exception as e:
        print(f"✗ LogEntry test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_color_provider():
    """Testa ClassColorProvider."""
    print("\nTesting ClassColorProvider...")
    
    try:
        from plugins.logcat.core.color.class_color_provider import ClassColorProvider
        
        provider = ClassColorProvider()
        color1 = provider.get_color("MyClass")
        color2 = provider.get_color("MyClass")
        
        # Deve ser determinístico
        assert color1 == color2
        assert color1.startswith("#")
        assert len(color1) == 7
        
        print("✓ ClassColorProvider deterministic coloring works")
        return True
    
    except Exception as e:
        print(f"✗ ClassColorProvider test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_key_colors():
    """Testa ToolKeyColorProvider."""
    print("\nTesting ToolKeyColorProvider...")
    
    try:
        from plugins.logcat.core.color.tool_key_color_provider import ToolKeyColorProvider
        
        provider = ToolKeyColorProvider()
        color = provider.get_color("system")
        assert color == "#FF6B6B"
        print("✓ ToolKeyColorProvider default colors work")
        
        provider.set_color("custom_tool", "#ABCDEF")
        assert provider.get_color("custom_tool") == "#ABCDEF"
        print("✓ ToolKeyColorProvider custom colors work")
        
        return True
    
    except Exception as e:
        print(f"✗ ToolKeyColorProvider test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_filter_engine():
    """Testa LogFilterEngine."""
    print("\nTesting LogFilterEngine...")
    
    try:
        from plugins.logcat.core.model.log_entry import LogEntry
        from plugins.logcat.core.filter.log_filter_engine import LogFilterEngine
        
        # Criar dados de teste
        entries = []
        for i in range(5):
            json_line = f'{{"ts": "2026-01-22T11:28:5{i}", "level": "INFO", "tool": "system", "class": "TestClass", "msg": "Message {i}", "data": {{}}}}'
            entry = LogEntry.from_json_line(json_line, i)
            if entry:
                entries.append(entry)
        
        engine = LogFilterEngine()
        
        # Teste de filtro de texto
        engine.set_text_filter("Message 1")
        filtered = engine.apply(entries)
        assert len(filtered) >= 1
        print("✓ LogFilterEngine text filtering works")
        
        # Teste de obter valores únicos
        levels = engine.get_unique_levels(entries)
        assert "INFO" in levels
        print("✓ LogFilterEngine get_unique_levels works")
        
        return True
    
    except Exception as e:
        print(f"✗ LogFilterEngine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("LOGCAT MODULE VALIDATION")
    print("=" * 60)
    
    all_ok = True
    all_ok = test_imports() and all_ok
    all_ok = test_log_entry() and all_ok
    all_ok = test_color_provider() and all_ok
    all_ok = test_tool_key_colors() and all_ok
    all_ok = test_filter_engine() and all_ok
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)
    
    sys.exit(0 if all_ok else 1)
