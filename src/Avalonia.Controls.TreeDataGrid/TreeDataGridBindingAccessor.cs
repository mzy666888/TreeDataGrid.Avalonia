using System;
using System.Globalization;
using Avalonia.Data;

namespace Avalonia.Controls
{
    internal sealed class TreeDataGridBindingAccessor : IDisposable
    {
        private readonly IDisposable _bindingDisposable;
        private readonly BindingExpressionBase? _expression;
        private readonly TreeDataGridBindingProbe _probe = new();
        private readonly BindingMode _mode;
        private Type? _inferredType;
        private bool _sampleValueWasNull;

        public TreeDataGridBindingAccessor(BindingBase binding, object? sampleModel = null)
        {
            _expression = _probe.Bind(TreeDataGridBindingProbe.ValueProperty, binding);
            _bindingDisposable = _expression;
            _mode = GetMode(binding);

            if (sampleModel is not null)
            {
                var sampleValue = Read(sampleModel);
                _sampleValueWasNull = sampleValue is null;
            }
        }

        public bool CanWrite => _mode is BindingMode.TwoWay or BindingMode.OneWayToSource;
        public bool SampleValueWasNull => _sampleValueWasNull;

        public static Func<TModel, string?>? TryCreateTextSelector<TModel>(BindingBase? binding)
            where TModel : class
        {
            if (binding is null)
                return null;

            var accessor = new TreeDataGridBindingAccessor(binding);
            return model => accessor.ReadAsString(model);
        }

        public object? Read(object model)
        {
            SetModel(model);
            _expression?.UpdateTarget();
            var value = NormalizeValue(_probe.Value);

            if (value is not null)
                _inferredType ??= value.GetType();

            return value;
        }

        public string? ReadAsString(object model)
        {
            return Read(model)?.ToString();
        }

        public bool ReadAsBoolean(object model)
        {
            return ConvertToBoolean(Read(model));
        }

        public bool? ReadAsNullableBoolean(object model)
        {
            return ConvertToNullableBoolean(Read(model));
        }

        public void Write(object model, object? value)
        {
            if (!CanWrite)
                return;

            SetModel(model);
            _probe.SetCurrentValue(TreeDataGridBindingProbe.ValueProperty, ConvertForSource(value));
            _expression?.UpdateSource();
            _expression?.UpdateTarget();

            var writtenValue = NormalizeValue(_probe.Value);

            if (writtenValue is not null)
                _inferredType ??= writtenValue.GetType();
        }

        public void Dispose()
        {
            _bindingDisposable.Dispose();
        }

        private static BindingMode GetMode(BindingBase binding)
        {
            return binding switch
            {
                Binding x => NormalizeMode(x.Mode),
                ReflectionBinding x => NormalizeMode(x.Mode),
                CompiledBinding x => NormalizeMode(x.Mode),
                MultiBinding x => NormalizeMode(x.Mode),
                _ => BindingMode.TwoWay,
            };
        }

        private static BindingMode NormalizeMode(BindingMode mode)
        {
            return mode == BindingMode.Default ? BindingMode.TwoWay : mode;
        }

        private static object? NormalizeValue(object? value)
        {
            return value switch
            {
                BindingNotification notification when notification.HasValue => NormalizeValue(notification.Value),
                BindingNotification => null,
                var x when ReferenceEquals(x, AvaloniaProperty.UnsetValue) => null,
                _ => value,
            };
        }

        private static bool ConvertToBoolean(object? value)
        {
            return ConvertToNullableBoolean(value) ?? false;
        }

        private static bool? ConvertToNullableBoolean(object? value)
        {
            value = NormalizeValue(value);

            return value switch
            {
                null => null,
                bool b => b,
                _ => (bool?)Convert.ChangeType(value, typeof(bool), CultureInfo.CurrentCulture),
            };
        }

        private object? ConvertForSource(object? value)
        {
            value = NormalizeValue(value);

            if (value is null)
                return null;

            var targetType = _inferredType;

            if (targetType is null)
                return value;

            var underlyingType = Nullable.GetUnderlyingType(targetType) ?? targetType;

            if (underlyingType.IsInstanceOfType(value))
                return value;

            if (underlyingType.IsEnum)
            {
                return value is string s
                    ? Enum.Parse(underlyingType, s, ignoreCase: true)
                    : Enum.ToObject(underlyingType, value);
            }

            if (value is IConvertible && typeof(IConvertible).IsAssignableFrom(underlyingType))
                return Convert.ChangeType(value, underlyingType, CultureInfo.CurrentCulture);

            return value;
        }

        private void SetModel(object model)
        {
            if (!ReferenceEquals(_probe.DataContext, model))
                _probe.DataContext = model;
        }
    }
}
