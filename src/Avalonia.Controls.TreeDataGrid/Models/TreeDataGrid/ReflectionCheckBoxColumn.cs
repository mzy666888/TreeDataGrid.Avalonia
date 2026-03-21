using System;
using Avalonia.Experimental.Data;

namespace Avalonia.Controls.Models.TreeDataGrid
{
    internal class ReflectionCheckBoxColumn : ColumnBase<object, bool?>
    {
        private readonly bool _isThreeState;

        public ReflectionCheckBoxColumn(
            object? header,
            Func<object, bool?> getter,
            Action<object, bool?>? setter,
            GridLength width,
            CheckBoxColumnOptions<object> options,
            bool isThreeState)
            : base(header, getter, CreateBinding(getter, setter), width, options)
        {
            _isThreeState = isThreeState;
        }

        public override ICell CreateCell(IRow<object> row)
        {
            return new CheckBoxCell(CreateBindingExpression(row.Model), Binding.Write is null, _isThreeState);
        }

        private static TypedBinding<object, bool?> CreateBinding(
            Func<object, bool?> getter,
            Action<object, bool?>? setter)
        {
            return new TypedBinding<object, bool?>
            {
                Read = getter,
                Write = setter,
                Links = new Func<object, object>[] { x => x },
            };
        }
    }
}
